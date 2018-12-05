from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
from queue import Queue
from threading import Thread, Event
from protocol_class import protocol
from time import sleep

class instagram(Thread):
    def __init__(self,username,password):
        super().__init__()
        self._credentials = [username,password]
        self._iqueue = Queue()  
        self._oqueue = None
        self._qaux = None
        self._alive = Event()
        self._client = None
 
    def auth(self,user_name1,password1):
        client = Client(
            auto_patch=True, authenticate=True,
            username= user_name1, password=password1)
        return client

    def process_msg(self,data): 
        if(data['field']=="comments"):
            id = data['value']['id']
            msg_text = data['value']['text']
            instagram_object = protocol("Instagram","Comment",id,id,msg_text,"")

        elif(data['field']=="mentions"):
            comment_id = data['value']['comment_id']
            '''media_id = data['value']['media_id']
            reference = self._client.media_info(media_id)
            reference == waiting return of webhook //app permission
            msg_text = data['value']['text']'''
            instagram_object = protocol("Instagram","Mention",comment_id,"username","msg_text","reference")
        return instagram_object

    def send_comment(self,msg_obj):
        self._client.post_comment(msg_obj.id,msg_obj.text)
    
    def run(self):
        #self._client = self.auth(self._credentials[0],self._credentials[1])
        self._alive.set()
        while self._alive:
            sleep(2)
            if not (self._qaux.empty()):
                data = self._qaux.get()
                msg = self.process_msg(data)
                if (msg != None):
                    self._oqueue.put(msg)
            if not (self._iqueue.empty()):
                msg_obj = self._iqueue.get() # get()
                self.send_comment(msg_obj)
