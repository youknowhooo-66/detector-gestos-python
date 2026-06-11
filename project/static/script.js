let currentActiveGesture = null;
const logList = document.getElementById('log-list');
const statusIndicator = document.getElementById('status-indicator');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

async function checkGesture() {
    try {
        const response = await fetch('/gesture_status');
        const data = await response.json();
        const detectedGesture = data.gesture;

        updateStatusUI(detectedGesture);
        handleRegistration(detectedGesture);
        
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
        statusText.textContent = 'Nenhum gesto detectado';
    }
}

function handleRegistration(gesture) {
    // Se um gesto foi detectado e é diferente do último gesto registrado (ou se não havia gesto)
    if (gesture && gesture !== currentActiveGesture) {
        registerGesture(gesture);
        currentActiveGesture = gesture;
    } 
    // Se nenhum gesto for detectado, resetamos o estado para permitir novo registro
    else if (!gesture) {
        currentActiveGesture = null;
    }
}

function registerGesture(gesture) {
    const now = new Date();
    const timestamp = now.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });

    const displayName = gesture === 'joinha' ? 'Joinha' : 'Hang Loose';
    
    const li = document.createElement('li');
    li.className = 'log-item';
    li.innerHTML = `
        <span class="log-text"><strong>${displayName}</strong> detectado — ${timestamp}</span>
    `;

    // Adiciona no topo da lista
    logList.insertBefore(li, logList.firstChild);
}

// Verifica o status a cada 300ms para maior fluidez
setInterval(checkGesture, 300);
