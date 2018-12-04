#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response
from http import HTTPStatus
from create_webhook import create_webhook
from subscribe_account import subscribe_account
import Twitter, hashlib, hmac, base64, os, logging, json
from requests_oauthlib import OAuth1Session
import urllib

	     
app = Flask(__name__)	
CONSUMER_KEY = 'NAK0slzNmfeT7ZOiC2CW40jUQ'
CONSUMER_SECRET = 'AkWgYk3zRXrmoj9wQIkCyanGEywamU6IHobR28D4NA5CS4AQlL'
ACCESS_TOKEN = '4693049767-Zyt4hmyIrNnaHVlZZUMokF1C9uCEdoJ2WRUWFav'
ACCESS_SECRET = 'NuEq2v8RWgJxgOAFjEhjtxcpwoHLG8EVc8haPMBryZxKC'
#generic index route    
@app.route('/')
def default_route():        
    return send_from_directory('www', 'index.html')    		      

#The GET method for webhook should be used for the CRC check
#TODO: add header validation (compare_digest https://docs.python.org/3.6/library/hmac.html)
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():

    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')

    return json.dumps(response)   
        
#The POST method for webhook should be used for all other API events
#TODO: add event-specific behaviours beyond Direct Message and Like
@app.route("/webhook", methods=["POST"])
def twitterEventReceived():		
    requestJson = request.get_json()

    #dump to console for debugging purposes
    print(json.dumps(requestJson, indent=4, sort_keys=True))
            
    if 'favorite_events' in requestJson.keys():
        #Tweet Favourite Event, process that
        likeObject = requestJson['favorite_events'][0]
        userId = likeObject.get('user', {}).get('id')          
            
        #event is from myself so ignore (Favourite event fires when you send a DM too)   
        if userId == "Mariozim0606":
            return ('', HTTPStatus.OK)
            
        Twitter.processLikeEvent(likeObject)
                        
    elif 'direct_message_events' in requestJson.keys():
        #DM recieved, process that
        eventType = requestJson['direct_message_events'][0].get("type")
        messageObject = requestJson['direct_message_events'][0].get('message_create', {})
        messageSenderId = messageObject.get('sender_id')   
        
        #event type isnt new message so ignore
        if eventType != 'message_create':
            return ('', HTTPStatus.OK)
            
        #message is from myself so ignore (Message create fires when you send a DM too)   
        if messageSenderId == "Mariozim0606":
            return ('', HTTPStatus.OK)
            
        Twitter.processDirectMessageEvent(messageObject)    
                
    else:
        #Event type not supported
        return ('', HTTPStatus.OK)
    
    return ('', HTTPStatus.OK)

                	    
if __name__ == '__main__':
    webhook_endpoint = "https://8834d55b.ngrok.io/webhook"
    # Bind to PORT if defined, otherwise default to 65010.
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    #create_webhook()
    #subscribe_account()
    twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_SECRET)
    url = 'https://api.twitter.com/1.1/account_activity/all/:env_name/subscriptions.json'
   
    r = twitter.post(url)
    print(r.text)
    app.run(debug=True)
