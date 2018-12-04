import json
from protocol_class import protocol
from dependences.secondary_functions import payload_send_DM_facebook
import traceback
import requests
from queue import Queue
from threading import Thread, Event
from time import sleep
import os
import facebook as fc

token = "EAAHsDbbXDc8BAO9hHBUDfVR1iUDZCfZBXOqoMtZA2VykXWTZA2D3UiDFkeedxteZBsA0pZASzlqe2znIdVrercbZB55xmrKWqUs6Svp6nCntURBMemhYtAjDoFHMPxWgEnH5q7XCoWOQyfoqMXC7nvooZAHby50JL8lZBtZAOV7kqmBnayEEVhrzel"
pageID = '2153856384731880'    #Page ID 

graph = fc.GraphAPI(access_token=token, version="3.0")
qaux = Queue()

class facebook(Thread):
    def auth(self):
        app_id = "541018622987727"
        canvas_url = "https://ddff9f6f.ngrok.io/auth-facebook"
        perms = ["manage_pages","publish_pages"]
        fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
        print(fb_login_url)

    def __init__(self,page_token):
        super().__init__()
        self._iqueue = Queue()
        self._oqueue = None
        self._qaux = None
        self._alive = Event()
        self._page_token = page_token

    def process_msg(self,json):
        if (json!= None and json != protocol):
            #r = requests.get("https://graph.facebook.com/v3.2/{}".format("2167833400000845"))
            if ("feed" in json):
                text = json['value']['message']
                ID = json['post_id']
                #reference = return of post_id request.  
                facebook_object = protocol("Facebook","Comment", ID,"",text,"")
                return facebook_object
            elif(json['object'] == "page" and "messaging" in json['entry'][0]):
                if('message' not in json['entry'][0]['messaging'][0] or pageID  == json['entry'][0]['messaging'][0]['sender']['id']):
                    facebook_object = None
                else:            
                    text = json['entry'][0]['messaging'][0]['message']['text']
                    ID = json['entry'][0]['messaging'][0]['sender']['id']
                    info_user = graph.get_object(ID)
                    username = info_user['first_name']
                    facebook_object = protocol("Facebook","DirectMessage",ID,username,text,"")
                return facebook_object

    def send_dm(self,msg, token):
        payload = payload_send_DM_facebook(msg.id,msg.text)
        try:
            if(payload != {}): 
                requests.post("https://graph.facebook.com/v3.2/me/messages?access_token="+token,json=payload)
        except:
            print(traceback.format_exc())

    def comment_status(self,msg_obj):
        pass

    def send(self,msg_obj):
        if(msg_obj.type == "DirectMessage"):
            self.send_dm(msg_obj, token)

        elif(msg_obj.type == "Comment"):
            self.comment_status(msg_obj)

    def run(self):
        self._alive.set()
        while self._alive:
            sleep(2)
            if not (self._iqueue.empty()):
                msg_obj = self._iqueue.get() # get()
                self.send(msg_obj)
            if not (self._qaux.empty()):
                data = self._qaux.get()
                msg = self.process_msg(data)
                if (msg != None):
                    self._oqueue.put(msg)

