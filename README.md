# Soundcloud Integration for Alexa
Use alexa to control your music from soundcloud

## Introduction
This is how a guide on how to write a custom skill that plays music on the amazon echo. Amazon Echo offers a few music services (like pandora or prime music or spotify), but unfortunately not soundcloud. Furthermore amazon does not allow to develop music application. The support to play mp3 files is very limited.
So, here is the hack-around:

## Setup

The following components are required.

- Local Server (your home computer, or raspberry pi, must support bluetooth and port must be open)
- AWS Lambda (handle Alexa Interaction)
- Amazon Echo Configuration

First we pair the Echo and our local server with bluetooth. Then we ask alexa to ask our custom skill to play music. The custom skill leverages aws lambda to make a request to our local server. Since our server is paired with alexa, we will hear the sound on the alexa.  

### Local Server

Folder: `/raspberry`

- `npm install`
- `sudo su` //port 80 requires sudo
- `export SOUNDCLOUD_ALEXA_BRIDGE_CLIENT_ID=1a23b4c56` //replace with client id from four soundcloud app
- `nodemon index.js`
- Go to your router settings and forward port 80 of your server

### AWS Lambda

Folder: `aws_lambda`

- create new application, use python 2.7 as enviroment
- copy content from `app.py` to `code`
- replace `access_token = None` with `access_token = "your soundcloud token"` (Account Linking in progress, see Future Work)
- replace `base_url` in Server with the ip address from your server
- save

### Amazon Echo

Folder: `alexa`

- create a new alexa skill https://developer.amazon.com/edw/home.html
- copy `intent_schema.json` to Interaction Model > Intent Schema
- copy `sample_utterances.txt` to Interaction Model > Sample Utterances
- copy the name of your aws lambda function to Configuration > Endpoint


## How to use

- "Alexa, pair bluetooth" (always the first step)
- Pair your local server with alexa
- "Alexa, open Soundcloud"
-  "Play from My Favorites"
- "Stop"
- "Skip | Play next"
- "What is the name of the Track?"
- "Volume up, Volume down" (no custom skill invocation necessary since we are playing via bluetooth)


## Future Work

- Account Linking
- Add Playlists, Stream, Charts
- Shuffle Function
- Fadeout/Stop in x seconds Function









