var net = require('net');

var HOST = '127.0.0.1';
var PORT = 1234;

var stdin = process.openStdin();
var client = new net.Socket();


stdin.addListener('data', function(d) {
    client.write('run 1 matching');
})

client.connect(PORT, HOST, function() {
    console.log('Client connected to: ' + HOST + ':' + PORT);
    //Write a message to the socket as soon as the client is
    //connected, the server will receive and respond
    client.write('establish connection');
});

client.on('data', function(data) {
    console.log('Client received: ' + data);
});

client.on('close', function() {
    console.log('Client closed');
});

client.on('error', function(err) {
    console.error(err);
});

