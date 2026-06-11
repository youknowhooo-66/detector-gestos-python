let lastAlertTime = 0;
const COOLDOWN_MS = 3000;
let lastGesture = null;

const statusIndicator = document.getElementById('status-indicator');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

async function checkGesture() {
    try {
        const response = await fetch('/gesture_status');
        const data = await response.json();

        if (data.gesture) {
            updateUI(data.gesture);
            triggerAlert(data.gesture);
        } else {
            updateUI(null);
        }
    } catch (error) {
        console.error('Erro ao buscar status:', error);
    }
}

function updateUI(gesture) {
    if (gesture === 'joinha') {
        statusIndicator.className = 'status active';
        statusDot.textContent = '🟢';
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

function triggerAlert(gesture) {
    const now = Date.now();
    // Only alert if cooldown passed AND it's a new gesture detection (or same after cooldown)
    if (now - lastAlertTime > COOLDOWN_MS) {
        lastAlertTime = now;
        if (gesture === 'joinha') {
            alert('👍 Joinha reconhecido com sucesso!');
        } else if (gesture === 'hang_loose') {
            alert('🤙 Hang Loose reconhecido! Uhuuu!');
        }
    }
}

// Check every 500ms
setInterval(checkGesture, 500);
