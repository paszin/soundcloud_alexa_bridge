// Create an app
var Player = require('player');
var server = require('diet');
var app = server();
app.listen('http://0.0.0.0:80');
var player;
var client_id = process.env["SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID"];
if (!client_id) {throw "Missing Client id in enviroment. To fix this run export SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID=1-wdwd-3434-fdf"}

app.header(function ($) {
    console.log($.header)
    console.log("Header Host", $.header("host"));
    console.log("Header Authorization", $.header("authorization"));
    //reject if not authorized
    //$.failure()
    $.return()
});

app.get('/play', function ($) {
    var links = $.query.links.split(",");
    links = links.map((url) => url + "?client_id=" + client_id);
    console.log("links:", links);
    if (!!player) {
        links.forEach((link) => player.add(link));
        $.end('added to player');
    } else {
        player = new Player(links);
        player.play();
        $.end('new player');
    }
});


app.get('/stop', function ($) {
    player.pause();
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
    player.next();
    $.end('next');
});


function play(source) {}