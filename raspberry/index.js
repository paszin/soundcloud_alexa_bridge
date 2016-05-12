// Create an app
var Player = require('player');
var server = require('diet');
var app = server();
app.listen('http://0.0.0.0:80');
var player;


app.header(function ($) {
    console.log($.header)
    console.log("Header Host", $.header("host"));
    console.log("Header Authorization", $.header("authorization"));
    //reject if not authorized
    //$.failure()
    $.return()
});

app.get('/play', function ($) {
    console.log($.query.link);
    player = new Player($.query.link);
    player.play();
    $.end('playing');
});


app.get('/stop', function ($) {
    player.stop();
    $.end('stop');
});

app.get('/volume', function ($) {
    player.setVolume($.query.value);
    $.end('volume');
});

app.get('/info', function ($) {
    $.end('info');
});

app.get('/next', function ($) {
    $.end('next');
});


function play(source) {}