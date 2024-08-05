const socket = io();

document.getElementById('send-button').onclick = () => {
const message = document.getElementById('message-input').value;
socket.emit('send_message', message);
document.getElementById('message-input').value = '';
};

socket.on('receive_message', (message) => {
const chat = document.getElementById('chat');
const messageElem = document.createElement('div');
messageElem.textContent = message;
chat.appendChild(messageElem);
chat.scrollTop = chat.scrollHeight;
});
document.getElementById('send-button').onclick = (event) => {
    event.preventDefault();
    const message = document.getElementById('message-input').value;
    if (message.trim()) {  // Avoid sending empty messages
        socket.emit('send_message', message);
        document.getElementById('message-input').value = '';
    }
};
