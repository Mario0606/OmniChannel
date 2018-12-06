from protocol_class import protocol
import json as js
from queue import Queue
from threading import Thread, Event
from requests_oauthlib import OAuth1Session
from dependences.twitter_listener_class import listener
from dependences.create_webhook_twitter import create_webhook_twitter
from dependences.subscribe_webhook_twitter import subscribe_webhook
from tweepy import API
from TwitterAPI import TwitterAPI
import requests
from time import sleep

class twitter(Thread):
    def __init__(self,auth,request,app_envname,webhook_url):
        super().__init__()
        self._webhookUrl = webhook_url
        self._request = request
        self._auth = auth
        self._api = API(auth)
        self._env_name = app_envname
        self._iqueue = Queue()
        self._oqueue = None
        self._qaux = None
        self._qaux = Queue()
        self._alive = Event()
   
    def webhook(self):
        t_request = OAuth1Session(self._auth.consumer_key,
                        client_secret=self._auth.consumer_secret,
                        resource_owner_key=self._auth.access_token,
                        resource_owner_secret=self._auth.access_token_secret)
        r = t_request.get('https://api.twitter.com/1.1/account_activity/all/webhooks.json')
        json = js.loads(r.text)
        if (len(json['environments'][0]['webhooks'])==0):
            api = TwitterAPI(self._auth.consumer_key,
                        self._auth.consumer_secret,
                        self._auth.access_token,
                        self._auth.access_token_secret)
            create_webhook_twitter(api,self._env_name,self._webhookUrl)
            subscribe_webhook(api,self._env_name)


    def process_msg(self,dict1): 
        '''Transform Twitter response(parameter:json) in protocol object'''
        if (dict1!= None):
            if("in_reply_to_status_id" in dict1):
                text = dict1["text"]
                Id = dict1['id']
                username = dict1['user']['screen_name']
                Id_send = dict1["user"]["id"]
                status = dict1["in_reply_to_status_id_str"]
                status_reference = self._api.get_status(Id)
                status_reference = status_reference._json["text"]
                twitter_object = protocol("Twitter","Comment",Id,username,text,status_reference) 
            elif("target" in dict1):
                text = dict1['message_data']['text']
                Id = dict1['sender_id']
                username = self._api.get_user(Id)._json['screen_name']
                twitter_object = protocol("Twitter","DirectMessage",Id,username,text,"") 
        return twitter_object

    def send_comment(self, msg_obj):
        '''post comment in a status
        paramers: msg_obj= object of protocol class
        status - msg_obj '''
        self._api.update_status("@"+msg_obj.username+" "+ msg_obj.text,in_reply_to_status_id=msg_obj.id)
    
    def send_direct_message(self,id_receiver,text):
        messageobject = {
        "event": {
            "type": "message_create",
            "message_create": {
            "target": {
                "recipient_id": id_receiver
            },
            "message_data": {
                "text": text
            }
            }
        }
        }
        self._api.send_direct_message_new(messageobject)
    
    def send(self,msg):
        if(msg.type == "Comment"):
            self.send_comment(msg)
        elif(msg.type == "DirectMessage"):
            self.send_direct_message(msg.id,msg.text)

    def run(self):
        self.webhook()
        self._alive.set()
        while self._alive:
            sleep(2)
            if not (self._qaux.empty()):
                msg = self._qaux.get()
                pmsg = self.process_msg(msg)
                self._oqueue.put(pmsg)
            if not (self._iqueue.empty()):
                msg = self._iqueue.get() # get()
                self.send(msg)
