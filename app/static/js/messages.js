// const chatMessages = document.getElementById("chat-messages");
// const messageInput = document.getElementById("message-input");
// const sendButton = document.getElementById("send-button");

// const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
// const wsURL = `${wsProtocol}${window.location.host}/messages?username=${username}`;

// const socket = new WebSocket(wsURL);

// socket.onopen = (event) => {
//     console.log("WebSocket connection opened.");
// };

// socket.onmessage = (event) => {
//     const message = JSON.parse(event.data);
//     displayMessage(message);
// };

// sendButton.addEventListener("click", () => {
//     const message = messageInput.value;
//     if (message.trim() !== "") {
//         socket.send(message);
//         messageInput.value = "";
//     }
// });

// function displayMessage(message) {
//     const messageElement = document.createElement("li");
//     messageElement.innerHTML = `
//         <p>${message.timestamp} - <strong>${message.username}:</strong> ${message.message}</p>
//     `;
//     chatMessages.appendChild(messageElement);
// }

// // Kur pranoni një mesazh nga serveri, ruani atë në localStorage
// function storeMessage(message) {
//     const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
//     messages.push(message);
//     localStorage.setItem('chatMessages', JSON.stringify(messages));
//   }
  
//   // Kur faqja është ngarkuar, ngarkoni mesazhet nga localStorage (nëse ka)
//   window.addEventListener('load', () => {
//     const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
//     // Përdorni messages për të paraqitur mesazhet në faqe
//   });
  




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
    storeMessage(message); // Store the received message in localStorage
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

// When you receive a message from the server, store it in localStorage
function storeMessage(message) {
    const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
    messages.push(message);
    localStorage.setItem('chatMessages', JSON.stringify(messages));
}

// When the page is loaded, load messages from localStorage (if any) and display them
window.addEventListener('load', () => {
    const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
    messages.forEach(message => {
        displayMessage(message);
    });
});
