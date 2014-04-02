var express = require('express'),
    app = express(),
    server = require('http').createServer(app),
    io = require('socket.io').listen(server);

var clients = {};

app.use(express.urlencoded());
server.listen(9999);

app.post('/:sessionId/', function (req, res) {
    var sessionId = req.params.sessionId;
    var socket = clients[sessionId];
    socket.emit('notify', JSON.parse(req.body.thumbs))
    res.end('Notification Pushed.');
});

io.sockets.on('connection', function (socket) {
    // Set client id.
    socket.on('setSessionCookie', function (sessionId) {
        clients[sessionId] = socket;
    });

});