"""
"""

from __future__ import print_function
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import os

## Configuration
SOUNDCLOUD_ACCESS_TOKEN = "your token"
SERVER_PUBLIC_URL = "http://you.org"
AMAZON_APPLICATION_ID = "amzn1.echo-sdk-ams.app.XXXXX"

class SoundcloudAPI:
    baseUrl = "https://api.soundcloud.com"
    #"http://paszin.zapto.org/

    def __init__(self, token):
        self.token = token

    def getMe(self):
        pass

    def getFavorites(self):
        """return a list with stream urls"""
        url = self.baseUrl + "/me/favorites?oauth_token=" + self.token
        print(url)
        data = urllib2.urlopen(url).read()
        favorites = json.loads(data)
        print("Found ", len(favorites), "Tracks")
        return favorites

class Server:
    
    @classmethod
    def get(self, path, params={}):
        baseUrl = SERVER_PUBLIC_URL
        #baseUrl = "http://127.0.0.1"
        queryParams = '&'.join([k+'='+v for k, v in params.items()])
        #return urllib2.urlopen(baseUrl + '/' + path + '?' + queryParams)
        opener = urllib2.build_opener()
        opener.addheaders = [('Authorization', AUTHORIZATION_SECRET)]
        return opener.open(baseUrl + '/' + path + '?' + queryParams)
#==============================================================================#

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    
    if (event['session']['application']['applicationId'] != AMAZON_APPLICATION_ID):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    mapping = {"PlayIntent": play, "StopIntent": stop, "VolumeIntent": volume, "InfoIntent": info, "NextIntent": nextf, "ShuffleIntent": shuffle}

    # Dispatch to your skill's intent handlers
    if intent_name in mapping.keys():
        return mapping[intent_name](intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def play(intent, session):
    token = getAccessToken(session)
    sc = SoundcloudAPI(token)
    source = getSlotValue(intent, "Source")

    if 'Source' in intent['slots']:
        source = intent['slots']['Source']['value']
    else:
        raise ValueError("Missing Slot Source")

    if source == "favorites":
        favs = sc.getFavorites()
        urls = [f['stream_url'] for f in favs]
    else:
        raise ValueError("Can not handle source " + source)

    resp = Server.get('play',{'links': ','.join(urls)})
    print(resp)
    print(resp.read())
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response())


def stop(intent, session):
    Server.get('stop');
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response())


def volume(intent, session):
    change = getSlotValue(intent, 'Change')
    session_attributes = {}
    speech_output = "This is not implemented. Please ask me without opening this skill"
    return build_response(session_attributes, build_speechlet_response(speech_output))



def info(intent, session):
    data = Server.get('info').read()
    print(data)
    info = json.loads(data)
    session_attributes = {}
    speech_output = "You are listening to " + info['title']
    card = {'title': "Soundcloud", 'content': speech_output}
    return build_response(session_attributes, build_speechlet_response(
        speech_output, card=card))


def nextf(intent, session):
    Server.get('next')
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response())

def shuffle(intent, session):
    Server.get('shuffle')
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response())
    
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    speech_output = "Yo, welcome to soundcloud";
    response = build_response(session_attributes, build_speechlet_response(
        speech_output, 
        card={'title': 'Welcome to Soundcloud', 'content': 'Please link your account'}, 
        should_end_session=False))
    response["response"]["card"]["type"] = "LinkAccount"
    return response


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you. Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    return build_response({}, build_speechlet_response(speech_output, should_end_session=True))


# --------------- Helpers that build all of the responses ----------------------

def getAccessToken(session):
    token = None
    if session.has_key("user") and session["user"].has_key("accessToken"):
        token = session["user"]["accessToken"]
    if not token:
        token = os.environ.get("accessToken")
        print("Take access Token from Enviroment")
    if not token:
        token = SOUNDCLOUD_ACCESS_TOKEN
        print("Take access Token from Code")
    if not token:
        raise ValueError("missing access token")
    return token

def getSlotValue(intent, name):
    if name in intent['slots']:
        return intent['slots'][name]['value'].lower()
    else:
        raise ValueError("Missing Slot " + source)

def build_speechlet_response(speech='ok', card=None, reprompt_text=None, should_end_session=True):
    resp = {}
    if speech:
        resp['outputSpeech'] = {
            'type': 'PlainText',
            'text': speech
        }
    if card:
        resp['card'] = {
            'type': card.get('type') or 'Simple',
            'title': card['title'],
            'content': card['content']
        }
    if reprompt_text:
        resp['reprompt'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        }
    resp['should_end_session'] = should_end_session
    return resp


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }