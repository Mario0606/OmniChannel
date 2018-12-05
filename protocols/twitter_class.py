from protocol_class import protocol
import json as js
from queue import Queue
from threading import Thread, Event
from dependences.twitter_listener_class import listener
from tweepy import API, Stream
import requests
from time import sleep

class twitter(Thread,listener):
    def __init__(self,auth):
        super().__init__()
        self._auth = auth
        self._api = API(auth)
        self._iqueue = Queue()
        self._oqueue = None
        self._qaux = Queue()
        self._alive = Event()
    
    def process_msg(self,json): 
        '''Transform Twitter response(parameter:json) in protocol object'''
        if (json!= None):
            if("in_reply_to_status_id" in json):
                json = js.loads(json)
                text = json["text"]
                ID = json['id']
                username = json['user']['screen_name']
                ID_send = json["user"]["id"]
                status = json["in_reply_to_status_id_str"]
                status_reference = self._api.get_status(ID)
                status_reference = status_reference._json["text"]
                twitter_object = protocol("Twitter","Comment",ID,username,text,status_reference) 
                return twitter_object
    
    def send_comment(self, msg_obj):
        '''post comment in a status
        paramers: msg_obj= object of protocol class
        status - msg_obj '''
        self._api.update_status("@"+msg_obj.username+" "+ msg_obj.text,in_reply_to_status_id=msg_obj.id)
    
    def send_direct_message(self,text, id_receiver):
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

    def on_data(self, data):
        print(data)
        self._qaux.put_nowait(data)
    
    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status, flush = True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))
    
    def on_error(self, status):
        print (status)
    
    def tserver(self):
        def _init_server(auth, l):
            twitterStream = Stream(auth, l)
            twitterStream.filter(track=['mariozim0606'])
        t_server = Thread(target=_init_server,args=(self._auth,self))
        t_server.start()
    
    def send(self,msg):
        if(msg.type == "Comment"):
            self.send_comment(msg)
        elif(msg.type == "DirectMessage"):
            self.send_direct_message(msg.id,msg.text)

    def run(self):
        self.tserver()
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
