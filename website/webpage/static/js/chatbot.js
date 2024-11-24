
function toggleChatbot() {
  const chatbotContainer = document.getElementById('chatbot-container');
  
  if (chatbotContainer.classList.contains('show')) {
      chatbotContainer.classList.remove('show');
      setTimeout(() => {
          chatbotContainer.style.display = 'none'; // Hide after transition
      }, 300); // Match the duration of the CSS transition
  } else {
      chatbotContainer.style.display = 'flex'; // Show the container
      setTimeout(() => {
          chatbotContainer.classList.add('show'); // Add class to trigger transition
      }, 10); // Small timeout to allow display to take effect
  }
}

  function sendMessage() {
    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value.trim();
    if (userMessage) {
      addMessage(userMessage, 'user');
      userInput.value = '';
      getBotResponse(userMessage);
    }
  }

  function addMessage(message, sender) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add(sender);
    messageContainer.textContent = message;
    document.getElementById('chatbot-messages').appendChild(messageContainer);
  }
  

  function getBotResponse(userMessage) {

    let botResponse = "I didn't understand that. Can you rephrase?";
    
    if (userMessage.toLowerCase().includes("services")) {
      botResponse = "We offer AI-based plant disease detection and care tips!";
    } else if (userMessage.toLowerCase().includes("help")) {
      botResponse = "I'm here to help with plant disease detection. Upload an image of your plant.";
    }
  
    setTimeout(() => {
      addMessage(botResponse, 'bot');
    }, 1000);
  }

  function closeChatbot() {
    const chatbotContainer = document.getElementById('chatbot-container');
    chatbotContainer.style.display = 'none';
  }
  

