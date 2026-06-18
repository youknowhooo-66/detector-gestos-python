import cv2
import os
import numpy as np

def test_save():
    # Cria uma imagem de teste (preta)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.putText(img, "TEST", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Define o caminho
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(base_dir, "project", "screenshots")
    
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        print(f"Pasta criada: {screenshots_dir}")
    
    filepath = os.path.join(screenshots_dir, "test_manual.jpg")
    print(f"Tentando salvar em: {filepath}")
    
    success = cv2.imwrite(filepath, img)
    if success:
        print(f"SUCESSO MANUAL: Arquivo criado em {filepath}")
    else:
        print("FALHA MANUAL: Não foi possível salvar.")

if __name__ == "__main__":
    test_save()
