const socket = new WebSocket("ws://localhost:8000/messages");

socket.onmessage = (event) => {
    const messagesDiv = document.getElementById("chat-messages");
    const message = JSON.parse(event.data);

    const messageDiv = document.createElement("div");
    messageDiv.innerText = `[${message.timestamp}] ${message.username}: ${message.content}`;
    messagesDiv.appendChild(messageDiv);
};

document.getElementById("send-button").addEventListener("click", () => {
    const input = document.getElementById("message-input");
    const message = input.value.trim();
    if (message !== "") {
        socket.send(JSON.stringify({ content: message }));
        input.value = "";
    }
});