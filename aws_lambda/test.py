import app

test_play_favorites = {
  "session": {
    "sessionId": "SessionId.1",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.1234"
    },
    "user": {
      "userId": "amzn1.ask.account.ABC"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.123",
    "timestamp": "2016-05-12T03:45:57Z",
    "intent": {
      "name": "PlayIntent",
      "slots": {
        "Source": {
          "name": "Source",
          "value": "favorites"
        }
      }
    },
    "locale": "en-US"
  },
  "version": "1.0"
}


app.lambda_handler(test_play_favorites, None)