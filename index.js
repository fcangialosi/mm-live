var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req,res) {
	res.sendFile(__dirname + '/index.html');
});

//var data = [];

io.on('connection', function(socket) {
	console.log('client connected');
	socket.on('disconnect', function() {
		console.log('client disconnected');
	});
	// var i = 0;
	//setInterval(function() {
	//	console.log(i);
	//	console.log(data);
	//	//io.emit('data', data[i]);
	//	i+=1;
	//}, 500);
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
		//data.push(d);
		//console.log(data);
	}
});
process.stdin.on('end', function() {
	console.log('end');
});


http.listen(8088, function() {
	console.log('listening on 8088');
});
