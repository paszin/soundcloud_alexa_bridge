# soundcloud_alexa_bridge
use alexa to control your music played from an external device

## Setup

- Raspberry Pi (run node server to play audio over aux output, must be accessible from the internet)
- AWS Lambda (handle Alexa Interaction)
- Alexa

## How to use

"Alexa, open Soundcloud"

"Play from My Favorites"

"Play from Playlist Chillout"

"Stop"

"Skip | Play next"

"What is the name of the Track?"

"Volume up, Volume down"


## Getting Started

- create a new AWS lambda application, use python 2.7 as enviroment
- create a new alexa skill https://developer.amazon.com/edw/home.html



#### Setup Server

- go to `raspberry`
- `npm install`
- `sudo su` //port 80 requires sudo
- `export SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID=1a23b4c56` //replace with client id from four soundcloud app
- `nodemon index.js`




