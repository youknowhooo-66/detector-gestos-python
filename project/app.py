import cv2
from flask import Flask, render_template, Response, jsonify, request, session, redirect, url_for
from hand_detector import HandDetector
from gesture_detector import GestureDetector
import sys
import os
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Necessário para o uso de sessions

# Configuração da pasta de screenshots
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

# Initialize detectors with error handling
try:
    detector = HandDetector()
    gesture = GestureDetector()
    print("Detectores inicializados com sucesso (MediaPipe Tasks API).")
except Exception as e:
    print(f"Erro crítico ao inicializar detectores: {e}")
    sys.exit(1)

# Global variables
current_gesture = None
machine_state = "DESLIGADA"

def save_screenshot_async(img, username, gesture_name):
    """Salva a screenshot em uma thread separada para não travar o vídeo."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{username}_{gesture_name}_{timestamp}.jpg"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        
        print(f"Tentando salvar screenshot em: {filepath}")
        
        # Garantir que a pasta existe logo antes de salvar
        if not os.path.exists(SCREENSHOTS_DIR):
            os.makedirs(SCREENSHOTS_DIR)
            print(f"Pasta criada no momento do salvamento: {SCREENSHOTS_DIR}")

        # Criar uma cópia da imagem para evitar problemas de concorrência
        img_copy = img.copy()
        success = cv2.imwrite(filepath, img_copy)
        
        if success:
            print(f"SUCESSO: Screenshot salva em {filepath}")
        else:
            print(f"FALHA: cv2.imwrite retornou False para {filepath}. Verifique permissões ou se o caminho é válido.")
            
    except Exception as e:
        print(f"ERRO CRÍTICO ao salvar screenshot: {str(e)}")
        import traceback
        traceback.print_exc()

def gen_frames():
    global current_gesture, machine_state
    last_saved_gesture = None
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a webcam.")
        return

    while True:
        success, img = cap.read()
        if not success:
            break
        
        try:
            # Detect hands and draw landmarks
            img = detector.find_hands(img)
            lm_list = detector.get_landmarks(img)
            
            # Update current gesture
            detected = gesture.get_gesture(lm_list)
            current_gesture = detected
            
            # Update machine state based on gesture
            if detected == "joinha":
                machine_state = "LIGADA"
            elif detected == "hang_loose":
                machine_state = "DESLIGADA"

            # Draw visual feedback on image
            if current_gesture:
                display_text = current_gesture.replace("_", " ").upper()
                cv2.putText(img, f"{display_text}!", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                # Salvar screenshot se for um novo gesto detectado
                if detected != last_saved_gesture:
                    # Obter username fora da thread para garantir acesso ao contexto da request se necessário
                    # (Embora aqui seja gen_frames que não tem contexto direto de request, 
                    # mas o username foi passado para a session em algum momento)
                    try:
                        # Em Response(gen_frames()), o contexto da request/session pode ser instável
                        # Vamos tentar capturar o username de forma segura
                        username = "operador"
                        if 'username' in session:
                            username = session['username']
                    except Exception as e:
                        print(f"Aviso: Não foi possível acessar a session no loop de frames: {e}")
                        username = "anonimo"

                    print(f"Iniciando thread para salvar gesto: {detected} por {username}")
                    
                    # Usar thread para salvar sem travar o loop de frames
                    thread = threading.Thread(target=save_screenshot_async, 
                                           args=(img.copy(), username, detected))
                    thread.setDaemon(True) # Garante que a thread não impeça o app de fechar
                    thread.start()
                    
                    last_saved_gesture = detected
            else:
                last_saved_gesture = None

            # Encode and yield frame
            ret, buffer = cv2.imencode('.jpg', img)
            if not ret:
                continue
                
            img_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
        except Exception as e:
            print(f"Erro no processamento de frame: {e}")
            continue

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/video_feed')
def video_feed():
    if 'username' not in session:
        return "Unauthorized", 401
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_status')
def gesture_status():
    global current_gesture, machine_state
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify({
        "gesture": current_gesture,
        "machine_state": machine_state,
        "username": session['username']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
