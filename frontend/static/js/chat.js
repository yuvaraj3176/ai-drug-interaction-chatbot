/**
 * Enhanced Chat Interface JavaScript
 * Member 2 Implementation
 */

let sessionId = '';
let chatHistory = [];
let isTyping = false;

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    setupEventListeners();
    loadChatHistory();
});

function initializeChat() {
    // Generate session ID if not exists
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // Focus on input
    document.getElementById('userInput').focus();
}

function setupEventListeners() {
    // Handle enter key
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Handle suggestion chips
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', function() {
            document.getElementById('userInput').value = this.textContent;
            sendMessage();
        });
    });
}

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message || isTyping) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    isTyping = true;
    
    // Send to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            message: message,
            session_id: sessionId 
        })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        isTyping = false;
        
        if (data.error) {
            addMessage('Sorry, an error occurred: ' + data.error, 'bot');
        } else {
            // Add bot response
            addMessage(data.response, 'bot');
            
            // If there are interactions, display them nicely
            if (data.interactions && data.interactions.length > 0) {
                displayInteractionResults(data.interactions);
            }
            
            // If there are drug suggestions, display them
            if (data.suggestions && data.suggestions.length > 0) {
                displaySuggestions(data.suggestions);
            }
            
            // Add to chat history
            chatHistory.push({
                user: message,
                bot: data.response,
                timestamp: new Date().toISOString()
            });
        }
    })
    .catch(error => {
        hideTypingIndicator();
        isTyping = false;
        addMessage('Sorry, connection error. Please try again.', 'bot');
        console.error('Error:', error);
    });
}

function addMessage(text, sender) {
    const container = document.getElementById('chatContainer');
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Format text with markdown-like syntax
    const formattedText = formatMessage(text);
    
    messageDiv.innerHTML = `
        ${formattedText}
        <div class="message-time">${time}</div>
    `;
    
    container.appendChild(messageDiv);
    scrollToBottom();
    
    // Add animation
    messageDiv.style.animation = 'fadeIn 0.3s ease-out';
}

function formatMessage(text) {
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert URLs to links
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Convert line breaks to <br>
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    indicator.style.display = 'block';
    scrollToBottom();
}

function hideTypingIndicator() {
    document.getElementById('typingIndicator').style.display = 'none';
}

function displayInteractionResults(interactions) {
    if (!interactions || interactions.length === 0) return;
    
    const container = document.getElementById('chatContainer');
    
    interactions.forEach(interaction => {
        const severity = interaction.severity || 'unknown';
        const severityClass = `severity-${severity}`;
        
        // Get severity icon
        let severityIcon = 'ℹ️';
        if (severity === 'severe') severityIcon = '🚫';
        else if (severity === 'moderate') severityIcon = '⚠️';
        else if (severity === 'mild') severityIcon = '📌';
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        messageDiv.innerHTML = `
            <div class="d-flex align-items-center mb-2">
                <span class="severity-badge ${severityClass} me-2">
                    ${severityIcon} ${severity.toUpperCase()}
                </span>
                <strong>${interaction.drug1} + ${interaction.drug2}</strong>
            </div>
            <div class="mb-2">${interaction.description}</div>
            <div class="mb-2"><em>💡 Recommendation: ${interaction.recommendation}</em></div>
            <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
        `;
        
        container.appendChild(messageDiv);
        messageDiv.style.animation = 'fadeIn 0.3s ease-out';
    });
    
    scrollToBottom();
}

function displaySuggestions(suggestions) {
    if (!suggestions || suggestions.length === 0) return;
    
    const container = document.getElementById('chatContainer');
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'message bot-message';
    
    let suggestionsHtml = '<div class="mb-2"><strong>You might also want to know about:</strong></div>';
    suggestionsHtml += '<div class="d-flex flex-wrap">';
    
    suggestions.forEach(suggestion => {
        suggestionsHtml += `
            <span class="suggestion-chip" onclick="useSuggestion('${suggestion}')">
                ${suggestion}
            </span>
        `;
    });
    
    suggestionsHtml += '</div>';
    suggestionsHtml += `<div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>`;
    
    suggestionsDiv.innerHTML = suggestionsHtml;
    container.appendChild(suggestionsDiv);
    scrollToBottom();
}

function useSuggestion(text) {
    document.getElementById('userInput').value = text;
    sendMessage();
}

function scrollToBottom() {
    const container = document.getElementById('chatContainer');
    container.scrollTop = container.scrollHeight;
}

function loadChatHistory() {
    fetch('/api/history')
    .then(response => response.json())
    .then(history => {
        if (history && history.length > 0) {
            const container = document.getElementById('chatContainer');
            container.innerHTML = ''; // Clear welcome message
            
            history.reverse().forEach(item => {
                addMessage(item.user, 'user');
                addMessage(item.bot, 'bot');
            });
        }
    })
    .catch(console.error);
}

function clearChat() {
    if (confirm('Clear all chat history?')) {
        document.getElementById('chatContainer').innerHTML = '';
        addMessage('👋 Chat cleared. How can I help you?', 'bot');
        chatHistory = [];
    }
}

// Export chat history
function exportChat() {
    const dataStr = JSON.stringify(chatHistory, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `chat_history_${new Date().toISOString().slice(0,10)}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}