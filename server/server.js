const express = require('express');
const app = express();
const port = 24912;
const server = require('http').Server(app);
const io = require('socket.io')(server);
const path = require('path');

// let rooms = {
//     "id":{
//         "id": "id",
//         "users": [{"id": "id", "mic": true, "camera": true, "hand": false}],
//     }
// };
let rooms = {};

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.redirect(`/select-device`)
});

app.get('/select-device/:roomid', (req, res) => {
    const filePath = path.join(__dirname, 'views', 'select-device.html');
    res.sendFile(filePath);
});

app.get('/room/:room', (req, res) => {
    const filePath = path.join(__dirname, 'views', 'room.html');
    res.sendFile(filePath);
});

io.on('connection', socket => {
    socket.on('join-room', (roomId, userId) => {
        socket.join(roomId);
        socket.to(roomId).emit('user-connected', userId);
        if (!rooms[roomId]) {
            rooms[roomId] = {
                "id": roomId,
                "users": [{"id": userId, "mic": true, "camera": true, "hand": false}],
            }
        } else {
            rooms[roomId].users.push({"id": userId, "mic": true, "camera": true, "hand": false});
        }
    });

    socket.on('disconnect', (roomId, userId) => {
        socket.to(roomId).emit('user-disconnected', userId)
    });

    socket.on('I-disconnect', (roomId, userId) => {
        socket.to(roomId).emit('user-disconnected', userId)
        if (!rooms[roomId]) return;
        rooms[roomId].users.forEach(user => {
            if (user.id === userId) {
                rooms[roomId].users.splice(rooms[roomId].users.indexOf(user), 1);
            }
        });
    });

    socket.on('mic-triggered', (roomId, userId) => {
        socket.to(roomId).emit('user-mic-triggered', userId)
        if (!rooms[roomId]) return;
        rooms[roomId].users.forEach(user => {
            if (user.id === userId) {
                user.mic = !user.mic;
            }
        });
    });

    socket.on('camera-triggered', (roomId, userId) => {
        socket.to(roomId).emit('user-camera-triggered', userId)
        if (!rooms[roomId]) return;
        rooms[roomId].users.forEach(user => {
            if (user.id === userId) {
                user.camera = !user.camera;
            }
        });
    });

    socket.on('hand-triggered', (roomId, userId) => {
        socket.to(roomId).emit('user-hand-triggered', userId)
        if (!rooms[roomId]) return;
        rooms[roomId].users.forEach(user => {
            if (user.id === userId) {
                user.hand = !user.hand;
            }
        });
    });

    socket.on('get-users', (roomId) => {
        rooms[roomId] ? socket.emit('users', rooms[roomId].users) : rooms[roomId] = {"id": roomId, "users": []};
    });

    socket.on('test', (roomId, text) => {
        socket.to(roomId).emit('user-test', text)
    });
});

server.listen(port);