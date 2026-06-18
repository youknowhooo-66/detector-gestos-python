# Detector de Gestos - Controle de Máquina

Este projeto utiliza inteligência artificial para simular o controle de uma máquina industrial através de gestos capturados pela webcam.

## 🚀 Funcionalidades

- **Autenticação de Operador:** Tela de login inicial para identificação do usuário.
- **Controle por Gestos:**
  - 👍 **Joinha:** Liga a máquina.
  - 🤙 **Hang Loose:** Desliga a máquina.
- **Simulação em Tempo Real:** Interface visual que reflete o estado da máquina (LIGADA/DESLIGADA) com animações dinâmicas.
- **Histórico de Operações:** Registro detalhado de quem executou a ação, qual gesto foi usado, o horário e o estado resultante da máquina.
- **Evidências Fotográficas:** Captura automática de screenshot (com landmarks desenhados) a cada ação registrada, salva na pasta `screenshots/` sem interromper a fluidez do vídeo.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, Flask.
- **Visão Computacional:** OpenCV, MediaPipe (Tasks API).
- **Frontend:** HTML5, Vanilla CSS3, JavaScript.

## 📋 Pré-requisitos

Certifique-se de ter o Python instalado e instale as dependências:

```bash
pip install -r requirements.txt
```

## 🏃 Como Executar

1. Navegue até a pasta do projeto:
   ```bash
   cd project
   ```
2. Execute o aplicativo:
   ```bash
   python app.py
   ```
3. Abra o navegador em `http://localhost:5000`.

## 📂 Estrutura de Pastas

- `app.py`: Servidor Flask e lógica principal.
- `hand_detector.py`: Wrapper para a API do MediaPipe.
- `gesture_detector.py`: Lógica de classificação dos gestos.
- `screenshots/`: Local onde as capturas de tela são armazenadas.
- `static/`: Arquivos CSS e JavaScript.
- `templates/`: Páginas HTML.

## 🧠 Detalhes Técnicos

### 1. Processamento de Vídeo
O backend utiliza OpenCV para capturar frames e MediaPipe para detectar os 21 landmarks da mão. O streaming para o navegador é feito via MJPEG.

### 2. Lógica Assíncrona de Screenshots
Para evitar travamentos na interface, o salvamento das imagens é realizado em threads separadas (`threading`). Cada captura inclui o nome do operador e o timestamp.

### 3. Máquina de Estados
O sistema rastreia a transição entre os gestos para evitar múltiplos registros e capturas acidentais de um mesmo gesto mantido na câmera.

---
**Desenvolvido para Desafio Técnico - 2026**
