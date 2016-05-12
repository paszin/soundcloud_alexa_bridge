// Create an app
var Player = require('player');
var server = require('diet');
var app = server();
app.listen('http://0.0.0.0:80');
var player;


app.header(function ($) {
    console.log($.header)
    console.log("Header Host", $.header("Host"));
    console.log("Header Authorization", $.header("Authorization"));
    //reject if not authorized
    //$.failure()
    $.return()
});

app.get('/play', function ($) {
    player = new Player($.params.link);
    player.play();
    $.end('playing');
});


app.get('/stop', function ($) {
        $.end('stop');
});

app.get('/volume', function ($) {
        $.end('volume');
});

app.get('/info', function ($) {
        $.end('info');
});

app.get('/next', function ($) {
        $.end('next');
});


function play(source) {}