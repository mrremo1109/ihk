const socket = io.connect('http://localhost:3000');
let currentReceiverId = null;
let currentReceiverName = null;

function openChat(receiverId, receiverName) {
    currentReceiverId = receiverId;
    currentReceiverName = receiverName;

    // Update chat header with the current receiver's name
    document.getElementById('chat-header-username').innerText = receiverName;

    // Clear previous messages
    document.getElementById('messages').innerHTML = '';

    // Join the room
    socket.emit('joinRoom', { room: `chat_{{ request.user.id }}_${receiverId}`, sender: "{{ request.user.username }}", receiver: receiverName });

    // Fetch previous messages
    fetch(`/chat/${receiverId}/messages/`)
        .then(response => response.json())
        .then(data => {
            const messagesContainer = document.getElementById('messages');
            data.forEach(message => {
                const newMessage = document.createElement('div');
                newMessage.className = `message ${message.sender === "{{ request.user.username }}" ? 'sent' : 'received'}`;
                newMessage.innerText = message.content;
                messagesContainer.appendChild(newMessage);
            });
        });
}

// Handle incoming messages
socket.on('receiveMessage', function(data) {
    if (data.receiver === currentReceiverName || data.sender === currentReceiverName) {
        const messagesContainer = document.getElementById('messages');
        const newMessage = document.createElement('div');
        newMessage.className = `message ${data.sender === "{{ request.user.username }}" ? 'sent' : 'received'}`;
        newMessage.innerText = data.content;
        messagesContainer.appendChild(newMessage);

        // Scroll to the bottom of the messages
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});

// Send message function
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const content = messageInput.value;

    if (content.trim() && currentReceiverId) {
        // Send message to the server for persistence
        fetch('/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ content: content, receiver: currentReceiverId })
        });

        // Emit message via Socket.IO
        socket.emit('sendMessage', {
            room: `chat_{{ request.user.id }}_${currentReceiverId}`,
            sender: "{{ request.user.username }}",
            receiver: currentReceiverName,
            content: content
        });

        // Clear the input
        messageInput.value = '';
    }
}
