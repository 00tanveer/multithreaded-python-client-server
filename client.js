var net = require('net');

var HOST = '127.0.0.1';
var PORT = 12345;

var client = new net.Socket();

client.connect(PORT, HOST, function() {
    console.log('Client connected to: ' + HOST + ':' + PORT);
    //Write a message to the socket as soon as the client is
    //connected, the server will receive and respond
    client.write('run 1 matching');
});

client.on('data', function(data) {
    console.log('Client received: ' + data);
});

client.on('close', function() {
    console.log('Client closed');
});

client.on('error', function() {
    console.error(err);
});

