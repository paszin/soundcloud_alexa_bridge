// Create an app
var Player = require('player');
var server = require('diet');
var app = server();
app.listen('http://0.0.0.0:80');
var player;


app.get('/play', function ($) {
    player = new Player($.params.link);
    player.play();
    $.end('playing');
});

function play(source) {}