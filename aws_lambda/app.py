"""
"""

from __future__ import print_function
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import os

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
        baseUrl = "http://paszin.zapto.org"
        #baseUrl = "http://127.0.0.1"
        queryParams = '&'.join([k+'='+v for k, v in params.items()])
        return urllib2.urlopen(baseUrl + '/' + path + '?' + queryParams)

#==============================================================================#

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    
    if (event['session']['application']['applicationId'] !=
             "amzn1.echo-sdk-ams.app.f2d582b0-58b6-440f-9951-50aceb0c9ad3"):
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

    mapping = {"PlayIntent": play, "StopIntent": stop, "VolumeIntent": volume, "InfoIntent": info, "NextIntent": nextf}

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
    card_title = "Playing"
    speech_output = "Playing "
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def stop(intent, session):
    Server.get('stop');
    session_attributes = {}
    card_title = "Playing stop"
    speech_output = "ok"
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def volume(intent, session):
    change = getSlotValue(intent, 'Change')
    if change in ['up', 'louder', 'higher']:
        current_volume = Server.get('volume')

    Server.get('volume', {'value': 1})
    session_attributes = {}
    card_title = "volume"
    speech_output = ""
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def info(intent, session):
    data = Server.get('info').read()
    print(data)
    info = json.loads(data)
    session_attributes = {}
    card_title = "Playing " 
    speech_output = "You are listening to " + info['title']
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def nextf(intent, session):
    Server.get('next')
    session_attributes = {}
    card_title = "Playing next"
    speech_output = "ok"
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Yo, welcome to soundcloud";
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Come on, say something!"
    should_end_session = False
    response = build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    print("response", response)
    response["response"]["card"]["type"] = "LinkAccount"
    return response


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you. Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------

def getAccessToken(session):
    token = None
    if session.has_key("user") and session["user"].has_key("accessToken"):
        token = session["user"]["accessToken"]
    if not token:
        token = os.environ.get("accessToken")
        print("Take access Token from Enviroment")
    if not token:
        raise ValueError("missing access token")
    return token

def getSlotValue(intent, name):
    if name in intent['slots']:
        return intent['slots'][name]['value'].lower()
    else:
        raise ValueError("Missing Slot " + source)

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }