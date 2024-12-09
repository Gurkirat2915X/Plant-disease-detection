// Global variable to store chat messages
let chatTranscript = []; // Array to store chat messages

function toggleChatbot() {
  const chatbotContainer = document.getElementById('chatbot-container');

  if (chatbotContainer.classList.contains('show')) {
      // If the chatbot is currently shown, just hide it immediately
      chatbotContainer.style.display = 'none'; // Hide without animation
      chatbotContainer.classList.remove('show'); // Remove show class
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
    chatTranscript.push(`User: ${userMessage}`); // Store user message in transcript
    userInput.value = '';
    getBotResponse(userMessage);
  }
}

function addMessage(message, sender) {
  const messageContainer = document.createElement('div');
  messageContainer.classList.add(sender); // 'user' or 'bot'
  messageContainer.textContent = message;
  document.getElementById('chatbot-messages').appendChild(messageContainer);
  
  // Scroll to the bottom of the messages
  const messagesContainer = document.getElementById('chatbot-messages');
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to the bottom
}

function getBotResponse(userMessage) {
  let botResponse = "I didn't understand that. Can you rephrase?";
  // Add the fetch call to the backend here
  if (userMessage.toLowerCase().includes("services")) {
    botResponse = "We offer AI-based plant disease detection and care tips!";
  } else if (userMessage.toLowerCase().includes("help")) {
    botResponse = "I'm here to help with plant disease detection. Upload an image of your plant.";
  }

  setTimeout(() => {
    addMessage(botResponse, 'bot');
    chatTranscript.push(`AgriBot: ${botResponse}`); // Store bot response in transcript
  }, 1000);
}

function closeChatbot() {
  const chatbotContainer = document.getElementById('chatbot-container');
  chatbotContainer.classList.add('hide'); // Add hide class for closing animation
  setTimeout(() => {
      chatbotContainer.classList.remove('show'); // Remove show class
      chatbotContainer.style.display = 'none'; // Hide after transition
      chatbotContainer.classList.remove('hide'); // Remove hide class
  }, 300); // Match the duration of the CSS transition
}

// Function to download the chat transcript
function downloadTranscript() {
  if (chatTranscript.length === 0) {
    alert("No messages to download."); // Alert if there are no messages
    return;
  }

  // Join the chat transcript into a single string
  const transcript = chatTranscript.join('\n');

  // Create a Blob from the transcript
  const blob = new Blob([transcript], { type: 'text/plain' });

  // Create a link element
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'chat_transcript.txt'; // Set the file name

  // Append the link to the body (required for Firefox)
  document.body.appendChild(link);

  // Programmatically click the link to trigger the download
  link.click();

  // Remove the link from the document
  document.body.removeChild(link);
}

// Add an event listener to the input field for the Enter key
document.getElementById('user-input').addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); // Prevent the default action (like form submission)
    sendMessage(); // Call the sendMessage function
  }
});