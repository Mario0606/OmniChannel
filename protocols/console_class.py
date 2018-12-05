from threading import Thread,Event
from queue import Queue
from protocol_class import protocol
from time import sleep

class console(Thread):
    def __init__(self):
        super().__init__()
        self._iqueue = Queue()
        self._oqueue_f = None
        self._oqueue_t = None
        self._oqueue_g = None
        self._oqueue_i = None
        self._oqueue_s = None
        self._alive = Event()

    def process(self, msg):
        print(msg.plataform,msg.username,msg.text)
        text = input()
        if(msg.plataform == "Facebook"):
            pattern_object = protocol("Facebook",msg.type,msg.id,msg.username,text,"")
        elif(msg.plataform == "Twitter"):
            pattern_object = protocol("Twitter",msg.type,msg.id,msg.username,text,"")
        elif(msg.plataform=="Gmail"):
            pattern_object = protocol("Gmail",msg.type,msg.id,msg.username,text,"")
        elif(msg.plataform == "Instagram"):
            pattern_object = protocol("Instagram",msg.type,msg.id,msg.username,text,"")
        elif(msg.plataform == "Skype"):
            pattern_object = protocol("Skype",msg.type,msg.id,msg.username,text,"")
        return pattern_object

    def run(self):
        self._alive.set()
        while self._alive: # probably wrong
            sleep(2)
            if not(self._iqueue.empty()):
                msg = self._iqueue.get() # get()
                pmsg = self.process(msg)
                if(pmsg.plataform == 'Facebook'):
                    self._oqueue_f.put_nowait(pmsg)
                elif(pmsg.plataform == 'Twitter'):
                    self._oqueue_t.put_nowait(pmsg)
                elif(pmsg.plataform == 'Gmail'):
                    self._oqueue_g.put_nowait(pmsg)
                elif(pmsg.plataform == 'Instagram'):
                    self._oqueue_i.put_nowait(pmsg)
                elif(pmsg.plataform == 'Skype'):
                    self._oqueue_s.put_nowait(pmsg)
                