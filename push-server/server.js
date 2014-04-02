var express = require('express'),
    app = express(),
    server = require('http').createServer(app),
    io = require('socket.io').listen(server);

// Make urlencoded module available to app.
app.use(express.urlencoded());

// Variable to keep track of currently connected Clients.
var clients = {};

// Setting Server to listen on port 9999.
server.listen(9999);

// Notification Route.
app.post('/:sessionId/', function (req, res) {
    // Reading sessionId from request object.
    var sessionId = req.params.sessionId;

    // Trying to locate socket client associated with sessionId.
    try {
        // Get client connected with the given ID.
        var socket = clients[sessionId];
        // Notify client and send thumbs urls.
        socket.emit('notify', JSON.parse(req.body.thumbs))
        // Respond to Media Server.
        res.end('Notification Acknowledged.');
    } catch (error) {
        res.end('Invalid SessionId.');
    }
});

io.sockets.on('connection', function (socket) {
    // Assigning sessionId to web socket.
    socket.on('setSessionCookie', function (sessionId) {
        clients[sessionId] = socket;
    });

});