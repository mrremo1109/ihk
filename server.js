const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*", // Allow cross-origin requests
        methods: ["GET", "POST"]
    }
});

app.use(cors());

let users = {};  // To store connected users by their userID

// Handling socket.io connections
io.on('connection', (socket) => {
    console.log('User connected: ', socket.id);

    // Handle user joining the chat and registering their userID
    socket.on('register', (userId) => {
        users[userId] = socket.id; // Map userId to socket.id
        console.log(`User ${userId} connected with socket id ${socket.id}`);
    });

    // Handle user sending a message
    socket.on('sendMessage', (data) => {
        const { senderId, receiverId, message } = data;
        
        if (users[receiverId]) {
            // Emit the message to the receiver
            io.to(users[receiverId]).emit('receiveMessage', {
                message,
                senderId
            });
        }

        // Save the message in the database (optional: connect to Django API)
    });

    // Handle user disconnect
    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
        // Remove user from the user list
        for (let userId in users) {
            if (users[userId] === socket.id) {
                delete users[userId];
                break;
            }
        }
    });
});

server.listen(3000, () => {
    console.log('Chat server is running on port 3000');
});