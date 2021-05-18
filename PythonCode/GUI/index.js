var http = require('http');
// var ForceGraph3D = require('3d-force-graph');
var fs = require('fs');
// var three = require('three');
var url = require('url');
var express = require('express')
var app = express()

app.get('/', function (request, response) {
  filename = './home.html';
  fs.readFile(filename, function (err, html) {
      if (err) {
      response.writeHead(404, {'Content-Type': 'text/html'});
      return response.end("404 Not Found");
    }
    response.writeHeader(200, {"Content-Type": "text/html"});
    response.write(html);
    response.end();
  });
})
app.use(express.static(__dirname));
app.listen(8080, "0.0.0.0")


// http.createServer(function(request, response) {
//   var q = url.parse(request.url, true);
//   var filename = "." + q.pathname;
//   if (q.pathname === '/')
//     filename = './home.html';
//   fs.readFile(filename, function (err, html) {
//       if (err) {
//       response.writeHead(404, {'Content-Type': 'text/html'});
//       return response.end("404 Not Found");
//     }
//     response.writeHeader(200, {"Content-Type": "text/html"});
//     response.write(html);
//     response.end();
//   });
// }).listen(1337, "127.0.0.1");

console.log('Server running at http://127.0.0.1:1337/');
//
// fs.readFile('./home.html', function (err, html) {
//     if (err) {
//         throw err;
//     }
//     http.createServer(function(request, response) {
//         response.writeHeader(200, {"Content-Type": "text/html"});
//         response.write(html);
//         response.end();
//     }).listen(1337, "127.0.0.1");
// });
// http.createServer(function (req, res) {
//   // res.writeHead(200, {'Content-Type': 'text/plain'});
//   // res.end('Hello World\n');
//   res.sendFile('absolutePathToYour/htmlPage.html');
// }).listen(1337, "127.0.0.1");
//
//
// console.log('Server running at http://127.0.0.1:1337/');
