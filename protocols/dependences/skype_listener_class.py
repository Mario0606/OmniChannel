from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeChatUpdateEvent
from queue import Queue

class SkypePing(SkypeEventLoop):
    def __init__(self,username,password):
        super(SkypePing, self).__init__(username, password)
        self._queue = Queue()

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent):
            self._queue.put(event)
        #if isinstance(event, SkypeChatUpdateEvent):
        #    print(event)
        