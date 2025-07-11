function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageElem = document.createElement('div');
    messageElem.classList.add('message');
    messageElem.innerHTML = `<span class="${sender}">${sender}:</span> ${text}`;
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    appendMessage('user', userMessage);
    inputField.value = '';

    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage('bot', data.response);
    })
    .catch(err => {
        appendMessage('bot', `Error: ${err.message}`);
    });
}