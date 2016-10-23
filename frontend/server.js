var http = require('http')
var parseUrl = require('parseurl')
var send = require('send')
 
var app = http.createServer(function onRequest (req, res) {
  send(req, parseUrl(req).pathname).pipe(res)
}).listen(3000)