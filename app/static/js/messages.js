const chatMessages = document.getElementById("chat-messages");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const wsURL = `${wsProtocol}${window.location.host}/messages?username=${username}`;

const socket = new WebSocket(wsURL);

socket.onopen = (event) => {
    console.log("WebSocket connection opened.");
};

socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    displayMessage(message);
};

sendButton.addEventListener("click", () => {
    const message = messageInput.value;
    if (message.trim() !== "") {
        socket.send(message);
        messageInput.value = "";
    }
});

function displayMessage(message) {
    const messageElement = document.createElement("li");
    messageElement.innerHTML = `
        <p>${message.timestamp} - <strong>${message.username}:</strong> ${message.message}</p>
    `;
    chatMessages.appendChild(messageElement);
}