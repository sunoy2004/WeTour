class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
        this.isTyping = false;
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })

        // Add welcome message
        this.addMessage("Sam", "Hello! I'm your travel assistant. How can I help you plan your next trip?");
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    addMessage(name, message) {
        const msg = { name, message };
        this.messages.push(msg);
        this.updateChatText(document.querySelector('.chatbox__support'));
    }

    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const chatbox = document.querySelector('.chatbox__support');
        const messagesContainer = chatbox.querySelector('.chatbox__messages');
        
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'messages__item messages__item--typing';
        typingIndicator.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        messagesContainer.appendChild(typingIndicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const chatbox = document.querySelector('.chatbox__support');
        const typingIndicator = chatbox.querySelector('.messages__item--typing');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        this.updateChatText(chatbox);
        textField.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // Simulate network delay
        setTimeout(() => {
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: JSON.stringify({ message: text1 }),
                mode: 'cors',
                headers: {
                  'Content-Type': 'application/json'
                },
              })
              .then(r => r.json())
              .then(r => {
                this.hideTypingIndicator();
                let msg2 = { name: "Sam", message: r.answer };
                this.messages.push(msg2);
                this.updateChatText(chatbox);
    
            }).catch((error) => {
                this.hideTypingIndicator();
                console.error('Error:', error);
                let errorMsg = { name: "Sam", message: "Sorry, I'm having trouble connecting. Please try again later." };
                this.messages.push(errorMsg);
                this.updateChatText(chatbox);
              });
        }, 1000);
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
        chatmessage.scrollTop = chatmessage.scrollHeight;
    }
}

// Initialize chatbox
const chatbox = new Chatbox();
chatbox.display();

// Function to submit trip plan to Firebase
async function submitTripPlan(planData) {
    try {
        // Check if user is authenticated
        const user = firebaseAuth.currentUser;
        if (!user) {
            throw new Error('User not authenticated');
        }
        
        // Add user ID to plan data
        planData.userId = user.uid;
        planData.createdAt = new Date();
        
        // Submit to Firebase Function
        const response = await fetch('https://us-central1-ghoomindia-355e9.cloudfunctions.net/submitTripPlan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${await user.getIdToken()}`
            },
            body: JSON.stringify(planData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Failed to submit trip plan');
        }
        
        return result;
    } catch (error) {
        console.error('Error submitting trip plan:', error);
        throw error;
    }
}