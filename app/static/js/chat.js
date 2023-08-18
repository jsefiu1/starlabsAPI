document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chat-messages');
  const userInput = document.getElementById('user-input');
  const sendButton = document.getElementById('send-button');

  sendButton.addEventListener('click', sendMessage);
  userInput.addEventListener('keyup', event => {
      if (event.key === 'Enter') {
          sendMessage();
      }
  });

  function sendMessage() {
      const userMessage = userInput.value.trim();
      if (userMessage === '') {
          return;
      }

      const userMessageElement = createMessageElement('user', userMessage);
      chatMessages.appendChild(userMessageElement);

      const formData = new FormData();
      formData.append('user_input', userMessage);

      fetch('/chat', {
          method: 'POST',
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          const assistantMessage = data.response;
          const assistantMessageElement = createMessageElement('assistant', assistantMessage);
          chatMessages.appendChild(assistantMessageElement);
      })
      .catch(error => {
          console.error(error);
      });

      userInput.value = '';
  }

  function createMessageElement(role, content) {
      const messageElement = document.createElement('div');
      messageElement.classList.add('message', role);
      messageElement.textContent = content;
      return messageElement;
  }
});