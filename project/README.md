# MVP: Detector de Joinha com Registro de Log

Este projeto é um MVP (Minimum Viable Product) de um sistema de Visão Computacional que reconhece o gesto de "joinha" pela webcam e mantém um registro histórico de cada detecção com o respectivo horário.

## 🚀 Objetivo
Criar um sistema capaz de detectar o gesto de "joinha" e "hang loose", registrando cada ocorrência em uma lista na tela apenas uma vez por gesto apresentado.

## ✨ Funcionalidades
- **Câmera em Tempo Real:** Visualização fluida do feed da webcam no navegador.
- **Detecção de Mãos:** Reconhecimento preciso de landmarks da mão utilizando MediaPipe.
- **Reconhecimento de Gestos:** Identificação específica de "Joinha" e "Hang Loose".
- **Lista de Registros:** Histórico dinâmico na tela mostrando: `Gesto detectado — HH:mm:ss`.
- **Regra de Unicidade:** O sistema registra o gesto apenas uma vez enquanto ele permanece na câmera, evitando duplicatas repetitivas.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python, Flask
- **Visão Computacional:** OpenCV, MediaPipe (Tasks API)
- **Frontend:** HTML5, CSS3 (Layout Responsivo), JavaScript (Vanilla)

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.14+
- Webcam

### Passo a Passo
1. **Ative o ambiente virtual:**
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Inicie o servidor:**
   ```powershell
   python app.py
   ```
4. **Acesse no navegador:**
   [http://localhost:5000](http://localhost:5000)

## 🧠 Explicação Técnica (Para o Tech Lead)

### 1. Funcionamento da Câmera
O backend (`app.py`) utiliza o OpenCV para capturar frames, processá-los com o MediaPipe e enviá-los via streaming multipart (MJPEG) para uma tag `<img>` no HTML.

### 2. Detecção do Gesto
A lógica está concentrada em `gesture_detector.py`. O sistema verifica a posição relativa dos landmarks:
- **Joinha:** Polegar aberto (acima da articulação) e demais dedos com as pontas abaixo das articulações médias (fechados).

### 3. Registro de Horário e Log
O frontend (`script.js`) consome uma API de status a cada 300ms. Quando um novo gesto é identificado:
- O JavaScript captura o horário local da máquina (`new Date()`).
- O log é inserido dinamicamente no topo da lista usando manipulação de DOM.

### 4. Evitando Registros Repetidos
Implementamos uma máquina de estados simples no frontend. Uma variável `currentActiveGesture` armazena o último gesto registrado. Um novo registro só é permitido se:
- O novo gesto for diferente do atual.
- O estado de "nenhum gesto" for detectado (reset), permitindo registrar o mesmo gesto novamente se ele for retirado e recolocado na câmera.

---
**Desenvolvido para Desafio Técnico - 2026**
