let currentActiveGesture = null;
const logList = document.getElementById('log-list');
const statusIndicator = document.getElementById('status-indicator');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const machineDisplay = document.getElementById('machine-display');
const currentUser = document.getElementById('current-user').textContent;

async function checkGesture() {
    try {
        const response = await fetch('/gesture_status');
        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }
        const data = await response.json();
        
        updateStatusUI(data.gesture);
        updateMachineUI(data.machine_state);
        handleRegistration(data.gesture, data.machine_state);
        
    } catch (error) {
        console.error('Erro ao buscar status:', error);
    }
}

function updateStatusUI(gesture) {
    if (gesture === 'joinha') {
        statusIndicator.className = 'status active';
        statusDot.textContent = '👍';
        statusText.textContent = 'Joinha detectado!';
    } else if (gesture === 'hang_loose') {
        statusIndicator.className = 'status active hang-loose';
        statusDot.textContent = '🤙';
        statusText.textContent = 'Hang Loose detectado!';
    } else {
        statusIndicator.className = 'status neutral';
        statusDot.textContent = '🔴';
        statusText.textContent = 'Aguardando gesto...';
    }
}

function updateMachineUI(state) {
    if (state === 'LIGADA') {
        machineDisplay.textContent = 'LIGADA';
        machineDisplay.className = 'machine-on';
    } else {
        machineDisplay.textContent = 'DESLIGADA';
        machineDisplay.className = 'machine-off';
    }
}

function handleRegistration(gesture, machineState) {
    // Registra apenas se o gesto mudou e não é nulo
    if (gesture && gesture !== currentActiveGesture) {
        registerAction(gesture, machineState);
        currentActiveGesture = gesture;
    } 
    // Reseta o gesto atual se nenhum gesto for detectado para permitir nova detecção do mesmo gesto
    else if (!gesture) {
        currentActiveGesture = null;
    }
}

function registerAction(gesture, machineState) {
    const now = new Date();
    const timestamp = now.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });

    const gestureName = gesture === 'joinha' ? 'Joinha' : 'Hang Loose';
    
    const li = document.createElement('li');
    li.className = 'log-item';
    li.innerHTML = `
        <div class="log-content">
            <span class="log-user">👤 ${currentUser}</span>
            <span class="log-time">🕒 ${timestamp}</span>
            <span class="log-gesture">👋 Gesto: <strong>${gestureName}</strong></span>
            <span class="log-machine">⚙️ Máquina: <strong>${machineState}</strong></span>
        </div>
    `;

    // Adiciona no topo da lista
    logList.insertBefore(li, logList.firstChild);
}

// Verifica o status a cada 300ms para maior fluidez
setInterval(checkGesture, 300);
