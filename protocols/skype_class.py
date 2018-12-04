from protocol_class import protocol
import json
from queue import Queue
from threading import Thread, Event
import requests
from time import sleep
from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeChatUpdateEvent
from dependences.skype_listener_class import SkypePing

class skype(Thread):
    def __init__(self,username,password):
        super().__init__()
        self._stream =  SkypePing(username,password)
        self._iqueue = Queue()
        self._oqueue = None
        self._alive = Event()

    def process_msg(self,data):     
        print(data)
        skype_object = protocol("Skype","DirectMessage","ID","id","","") 
        return skype_object
    
    def send_direct_message(self,text, id_receiver):
        pass

    def sserver(self):
        def _init_server():
            self._stream.loop()   
        s_server = Thread(target=_init_server)
        s_server.start()
    
    def send(self,msg):
        pass

    def run(self):
        self.sserver()
        self._alive.set()
        while self._alive:
            sleep(2)
            if not (self._stream._queue.empty()):
                msg = self._stream._queue.get()
                pmsg = self.process_msg(msg)
                self._oqueue.put(pmsg)
            if not (self._iqueue.empty()):
                msg = self._iqueue.get() # get()
                self.send(msg)
