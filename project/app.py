import cv2
from flask import Flask, render_template, Response, jsonify
from hand_detector import HandDetector
from gesture_detector import GestureDetector
import sys

app = Flask(__name__)

# Initialize detectors with error handling
try:
    detector = HandDetector()
    gesture = GestureDetector()
    print("Detectores inicializados com sucesso (MediaPipe Tasks API).")
except Exception as e:
    print(f"Erro crítico ao inicializar detectores: {e}")
    sys.exit(1)

# Global variable to store current gesture
current_gesture = None

def gen_frames():
    global current_gesture
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
            current_gesture = gesture.get_gesture(lm_list)
            
            # Draw visual feedback on image
            if current_gesture:
                display_text = current_gesture.replace("_", " ").upper()
                cv2.putText(img, f"{display_text}!", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

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
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_status')
def gesture_status():
    global current_gesture
    return jsonify({"gesture": current_gesture})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
