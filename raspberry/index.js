// Create an app
var Player = require('player');
var server = require('diet');
var request = require('request');
var app = server();
app.listen('http://0.0.0.0:80');
var player;
var client_id = process.env["SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID"];
if (!client_id) {throw "Missing Client id in enviroment. To fix this run export SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID=1-wdwd-3434-fdf"}

function extractSoundcloudId(url) {
    var path = url.split('/')
    return path[path.indexOf('tracks')+1]

}

function getSoundcloudInfo(id, callback) {
    request('https://api.soundcloud.com/tracks/' + id + '?client_id=' + client_id,
        function (error, response, body) {
            if (!error && response.statusCode == 200) {
                callback(JSON.parse(body));
            }
        });
}

app.header(function ($) {
    //console.log($.header)
    //console.log("Header Host", $.header("host"));
    //console.log("Header Authorization", $.header("authorization"));
    //reject if not authorized
    //$.failure()
    $.return()
});

app.get('/play', function ($) {
    if (!!player && !$.query.hasOwnProperty('links')) {
        player.play();
        return $.end('continue player');
    }
    var links = $.query.links.split(",");
    links = links.map((url) => url + "?client_id=" + client_id);
    console.log("links:", links);
    if (!!player) {
        links.forEach((link) => player.add(link));
        player.play();
        $.end('added to player');
    } else {
        player = new Player(links);
        player.play();
        player.current_track_index = 0;
        $.end('new player, playing ' + player.list[player.current_track_index]);
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
    var url = player.list[player.current_track_index];
    var id = extractSoundcloudId(url);
    getSoundcloudInfo(id, function(data) {$.json(data)});

});

app.get('/next', function ($) {
    if (player.current_track_index >= player.list.length - 1) {
        $.end('no more tracks');
    }
    player.next();
    player.current_track_index += 1;
    $.end('next ' + player.list[player.current_track_index]);
});

app.get('/playlist', function($) {
    $.json({'current_track_id': player.current_track_index, 'playlist': player.list})
})

function play(source) {}