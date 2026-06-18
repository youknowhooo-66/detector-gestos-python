# Histórico de Implementações - Detector de Gestos

Este documento registra a evolução do projeto, as decisões técnicas e as funcionalidades implementadas.

## Fase 1: Reconhecimento de "Joinha" (Base)
- Implementação inicial com MediaPipe Tasks API.
- Detecção de landmarks da mão.
- Lógica de gesto baseada na posição do polegar em relação aos outros dedos.
- Interface web básica com Flask e feed de vídeo.

## Fase 2: Controle de Máquina e Autenticação
- **Data:** 17 de Junho de 2026
- **Objetivo:** Simular o controle de uma máquina industrial via gestos.
- **Implementações:**
    - **Sistema de Login:** Adicionada tela de login simples (`login.html`) salvando o nome do operador na sessão do Flask.
    - **Controle de Estado:** Variável global para rastrear se a máquina está `LIGADA` ou `DESLIGADA`.
    - **Novo Gesto:** Implementado o gesto de **Hang Loose** (`[1, 0, 0, 0, 1]`) para desligar a máquina.
    - **Simulação Visual:** Painel na interface web que pulsa em verde quando a máquina está ligada e fica cinza quando desligada.
    - **Logs Detalhados:** Histórico na interface registrando Usuário, Horário, Gesto e Estado da Máquina.

## Fase 3: Evidências Visuais (Screenshots)
- **Objetivo:** Registrar visualmente cada ação realizada pelo operador.
- **Implementações:**
    - **Captura Automática:** O sistema detecta a mudança de estado e salva um frame da webcam.
    - **Processamento Assíncrono:** Uso de `threading` para salvar as imagens em disco sem travar o feed de vídeo (evitando freezes na UI).
    - **Nomenclatura Dinâmica:** Arquivos salvos com `NOME_GESTO_TIMESTAMP.jpg` na pasta `project/screenshots`.
    - **Robustez:** Implementada cópia profunda de frames (`img.copy()`) para evitar conflitos de memória entre a thread de exibição e a de salvamento.

## Notas Técnicas para Futuras Revisões:
- Os detectores são inicializados globalmente no `app.py`.
- O feed de vídeo usa o modo `multipart/x-mixed-replace`.
- A pasta `screenshots` é criada automaticamente se não existir.
- O segredo da sessão (`app.secret_key`) é necessário para o funcionamento do login.
