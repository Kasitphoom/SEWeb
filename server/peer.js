const { ExpressPeerServer } = require('peer');

const express = require('express');
const app = express();
const server = require('http').createServer(app);

// Set up PeerJS server
const peerServer = ExpressPeerServer(server, {
  debug: true, // Enable debug logs (optional)
});

// Mount PeerJS server on a specific path, e.g., '/peerjs'
app.use('/peerjs', peerServer);

// Start the server
const PORT = 24911;
server.listen(PORT, () => {
  console.log(`PeerJS server is running on port ${PORT}`);
});
