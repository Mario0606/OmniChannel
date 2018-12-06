"""
OmniChannel
"""
__version__ = '0.1'
__author__ = 'Iqnus'
#-*- coding: utf-8 -*-
from tweepy import OAuthHandler
from TwitterAPI import TwitterAPI
from queue import Queue

from facebook_class import facebook
from gmail_class import gmail
from console_class import console
from twitter_class import twitter
from instagram_class import instagram
from skype_class import skype
from flask import Flask, request, send_from_directory, make_response
from http import HTTPStatus
import hashlib, hmac, base64, os, logging, json
from flask import Flask, request,render_template

import json
import traceback
import os

#Archive of passwords
arq = open('/home/iqnus/passwords.json', 'rb')
text = arq.read()
text = json.loads(text)

#data of Twitter access 
ckey = text['twitter']['ckey']
csecret = text['twitter']['csecret']
atoken = text['twitter']['atoken']
asecret = text['twitter']['asecret']
webhook_url = text['twitter']['url']
env_name = text['twitter']['env_name']
myid_twitter = text['twitter']['current_id'] 

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterapi = TwitterAPI(ckey,csecret,atoken,asecret)

#data of Facebook access
page_token = text['facebook']['page_token']

#data of Skype access
usernameS = text['skype']['username']
passwordS = text['skype']['password']

#data of Instagram access
usernameI = text['instagram']['username']
passwordI = text['instagram']['password']

app = Flask(__name__)
qaux_F = Queue()
qaux_G = Queue()
qaux_I = Queue()
qaux_T = Queue()



'''Flask Routes '''
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():
    
    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(csecret, 'utf-8'),
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
    if 'tweet_create_events' in requestJson.keys():
        #Tweet Favourite Event, process that
        likeObject = requestJson['tweet_create_events'][0]
        userId = likeObject.get('user', {}).get('id')          
              
        #event is from myself so ignore (Favourite event fires when you send a DM too)   
        if userId == myid_twitter:
            return ('', HTTPStatus.OK)    
        qaux_T.put(likeObject)
                          
    elif 'direct_message_events' in requestJson.keys():
        #DM recieved, process that
        eventType = requestJson['direct_message_events'][0].get("type")
        messageObject = requestJson['direct_message_events'][0].get('message_create', {})
        messageSenderId = messageObject.get('sender_id')   
        
        #event type isnt new message so ignore
        if eventType != 'message_create':
            return ('', HTTPStatus.OK)
            
        #message is from myself so ignore (Message create fires when you send a DM too)   
        if messageSenderId == myid_twitter:
            return ('', HTTPStatus.OK)
             
        qaux_T.put(messageObject)
                
    else:
        #Event type not supported
        return ('', HTTPStatus.OK)
    
    return ('', HTTPStatus.OK)

@app.route('/gmail', methods=['GET', 'POST'])
def webhook_gmail():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_G.put(data)
            return "200"
            
        except:
            print(traceback.format_exc())

@app.route('/facebook', methods=['GET', 'POST'])
def webhook_facebook():      
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_F.put_nowait(data)
        except:
            print(traceback.format_exc())
    elif request.method == 'GET':                 
        if request.args.get('MessageBotTest') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"  

@app.route('/instagram', methods=['GET', 'POST'])
def webhook_instagram():      
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_I.put_nowait(data)
        except:
            print(traceback.format_exc())
    elif request.method == 'GET':                 
        if request.args.get('MessageBotTest') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing" 
@app.route("/googleddcf0dcf86bb8352.html/") 
def render(self):
    return render_template("googleddcf0dcf86bb8352.html")

@app.route('/auth-facebook')
def auth_facebook():
    if request.method == 'POST':
        data = json.loads(request.data.decode())
    elif request.method == 'GET':
        data = json.loads(request.data.decode())
    print(data)


if __name__=='__main__':
    
    twitter1 = twitter(auth,twitterapi,env_name,webhook_url)
    #facebook1 = facebook(page_token)
    #gmail1 = gmail() 
    #instagram1 = instagram(usernameI,passwordI)
    console1 = console()
    #skype1 = skype(usernameS,passwordS)

    console1._oqueue_t, twitter1._oqueue = twitter1._iqueue, console1._iqueue
    #console1._oqueue_f, facebook1._oqueue = facebook1._iqueue, console1._iqueue
    #console1._oqueue_g, gmail1._oqueue = gmail1._iqueue,console1._iqueue
    #console1._oqueue_g, instagram1._oqueue = instagram1._iqueue,console1._iqueue
    #console1._oqueue_s, skype1._oqueue = skype1._iqueue,console1._iqueue

    #facebook1._qaux = qaux_F
    #gmail1._qaux = qaux_G
    #instagram1._qaux = qaux_I
    twitter1._qaux = qaux_T
    #gmail1.start()
    #facebook1.start()
    twitter1.start()
    #instagram1.start()
    #skype1.start()
    console1.start()

    app.run(debug=True,port=65010)
