var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req,res) {
	res.sendFile(__dirname + '/mm-live-index.html');
});

io.on('connection', function(socket) {
	console.log('client connected');
	socket.on('disconnect', function() {
		console.log('client disconnected');
	});
});

process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(chunk) {
	var sp = chunk.split("\n");
	for (var i=0; i<sp.length-1; i++) {
		var spsp = sp[i].split(" ");
		var d = {	
			't' : parseFloat(spsp[0]),
			'sum' : parseFloat(spsp[1]),
			'delay' : parseFloat(spsp[2])
		}
		io.emit('data', d);
	}
});
process.stdin.on('end', function() {
	console.log('end');
});


http.listen(parseInt(process.argv[2]), function() {
	console.log('Visualization server listening on', process.argv[2]);
});
