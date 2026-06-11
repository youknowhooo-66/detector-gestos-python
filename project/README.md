# Desafio: Detector de Joinha (Python + Webcam + HTML)

Este projeto é uma aplicação de Visão Computacional em tempo real que utiliza a webcam para detectar mãos e reconhecer especificamente o gesto de "joinha" (polegar para cima). Desenvolvido com uma arquitetura moderna e robusta, utilizando **Python 3.14** e a **MediaPipe Tasks API**.

## Visão Geral

O sistema captura frames da webcam, processa-os utilizando inteligência artificial para localizar pontos de referência da mão e aplica uma lógica geométrica para identificar o gesto. Quando o "joinha" é detectado, a interface web é atualizada instantaneamente e um alerta visual é exibido ao usuário.

## Tecnologias Utilizadas

*   **Backend**: Python 3.14, Flask (Servidor Web)
*   **Visão Computacional**: OpenCV (Processamento de Imagem), MediaPipe 0.10.35+ (Tasks API)
*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
*   **Modelos**: MediaPipe Hand Landmarker (float16)

## Instalação e Execução

### Pré-requisitos
*   Python 3.14 instalado.
*   Webcam funcional.

### Passo a Passo

1.  **Crie o ambiente virtual:**
    ```powershell
    python -m venv venv
    ```

2.  **Ative o ambiente virtual (Windows):**
    ```powershell
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**
    ```powershell
    python app.py
    ```

*Nota: Na primeira execução, o sistema baixará automaticamente o modelo `hand_landmarker.task` (~15MB) do Google.*

## Acesso
Abra o navegador e acesse: [http://localhost:5000](http://localhost:5000)

## Como Funciona (Explicação Técnica)

### 1. Captura e Processamento
O sistema utiliza o **OpenCV** para acessar o buffer da webcam. Cada frame é convertido para RGB e enviado para o **Hand Landmarker** do MediaPipe.

### 2. Detecção de Landmarks
Diferente da API antiga, utilizamos a nova **MediaPipe Tasks API**, que retorna uma lista de 21 coordenadas (X, Y, Z) para cada mão detectada.

### 3. Identificação de Gestos
A classe `GestureDetector` aplica lógica geométrica para múltiplos gestos:
*   **Joinha**: Polegar (ID 4) aberto e outros 4 dedos fechados.
*   **Hang Loose (Shaka)**: Polegar (ID 4) e Mínimo (ID 20) abertos, com os três dedos centrais fechados.

### 4. Comunicação Frontend-Backend
*   **Vídeo**: Transmitido via streaming MJPEG na rota `/video_feed`.
*   **Status**: O JavaScript consulta a rota `/gesture_status` a cada **500ms** (polling).
*   **Feedback**: Quando o JSON retorna `thumbs_up: true`, o frontend altera a classe do indicador para verde e dispara um `alert()` com cooldown de 3 segundos para evitar loops de mensagens.

---
**Desenvolvedor:** Gemini CLI (Modo Auto-Edit)  
**Contexto:** Desafio Acadêmico / Apresentação Técnica
