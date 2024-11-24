document.addEventListener('DOMContentLoaded', function() {
  const messageContainer = document.createElement('div');
  messageContainer.classList.add('bot');
  messageContainer.textContent = "AgriBot: Hi! I'm AgriBot. How can I help you today?";
  document.getElementById('chatbot-messages').appendChild(messageContainer);})
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
      addMessage("User: "+userMessage, 'user');
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

    let botResponse = "AgriBot: I didn't understand that. Can you rephrase?";
    // add the fetch call to the backend here
    // csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const url = document.getElementById("chatbot-container").getAttribute("data-url")
    fetch(url,{
      method: 'POST',
      headers:{
        'Content-Type':'application/json',
        // 'X-CSRFToken':csrftoken,
      },
      body: JSON.stringify({'message':userMessage})
    }).then(response=>response.json()).then(data=>{
      addMessage(data.response,"bot")
    })
  
    
  }

  function closeChatbot() {
    const chatbotContainer = document.getElementById('chatbot-container');
    chatbotContainer.style.display = 'none';
  }
  

