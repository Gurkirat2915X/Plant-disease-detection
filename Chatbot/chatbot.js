
function toggleChatbot() {
    const chatbotContainer = document.getElementById('chatbot-container');
    chatbotContainer.style.display = chatbotContainer.style.display === 'block' ? 'none' : 'block';
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
  