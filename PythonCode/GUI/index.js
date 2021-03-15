var http = require('http');
// var ForceGraph3D = require('3d-force-graph');
var fs = require('fs');
var three = require('three')


fs.readFile('./index.html', function (err, html) {
    if (err) {
        throw err;
    }
    http.createServer(function(request, response) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        response.write(html);
        response.end();
    }).listen(1337, "127.0.0.1");
});
// http.createServer(function (req, res) {
//   // res.writeHead(200, {'Content-Type': 'text/plain'});
//   // res.end('Hello World\n');
//   res.sendFile('absolutePathToYour/htmlPage.html');
// }).listen(1337, "127.0.0.1");
//
//
console.log('Server running at http://127.0.0.1:1337/');
