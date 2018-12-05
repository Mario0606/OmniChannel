from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeChatUpdateEvent
from queue import Queue

class SkypePing(SkypeEventLoop):
    def __init__(self,username,password):
        super(SkypePing, self).__init__(username, password)
        self._queue = Queue()

    def onEvent(self, event):
        #print(event)
        if isinstance(event, SkypeNewMessageEvent)and not event.msg.userId == self.userId:
            print(event.msg.chat.user)
            user_name = event.msg.chat.user.name
            chatId = event.msg.chat.user.id
            text = event.msg.content
            self._queue.put((chatId, user_name, text))
        