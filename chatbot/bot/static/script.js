// script.js
document.addEventListener("DOMContentLoaded", function () {
    const chatbotContainer = document.getElementById("chatbot-container");
    const closeBtn = document.getElementById("close-btn");
    const sendBtn = document.getElementById("send-btn");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotMessages = document.getElementById("chatbot-messages");
  
    const chatbotIcon = document.getElementById("chatbot-icon");
    const closeButton = document.getElementById("close-btn");
  
    // Toggle chatbot visibility when clicking the icon
    // Show chatbot when clicking the icon
    chatbotIcon.addEventListener("click", function () {
      chatbotContainer.classList.remove("hidden");
      chatbotIcon.style.display = "none"; // Hide chat icon
    });
  
    // Also toggle when clicking the close button
    closeButton.addEventListener("click", function () {
      chatbotContainer.classList.add("hidden");
      chatbotIcon.style.display = "flex"; // Show chat icon again
    });
  
    sendBtn.addEventListener("click", sendMessage);
    chatbotInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  
    function sendMessage() {
      const userMessage = chatbotInput.value.trim();
      if (userMessage) {
        appendMessage("user", userMessage);
        chatbotInput.value = "";
        getBotResponse(userMessage);
      }
    }
  
    function appendMessage(sender, message) {
      const messageElement = document.createElement("div");
      messageElement.classList.add("message", sender);
      messageElement.textContent = message;
      chatbotMessages.appendChild(messageElement);
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
  
    function getCSRFToken() {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
          return value;
        }
      }
      return null;
    }

    async function getBotResponse(userMessage) {
        try {
          const csrfToken = getCSRFToken();
          const response = await fetch("http://localhost:8000/api/chat/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, // Include CSRF token
            },
            body: JSON.stringify({ message: userMessage }),
          });
      
          const data = await response.json();
          appendMessage("bot", data.response || "Oops! No response.");
        } catch (error) {
          console.error("Error fetching bot response:", error);
          appendMessage("bot", "Sorry, something went wrong.");
        }
      }
      
  });