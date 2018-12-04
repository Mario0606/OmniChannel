from skpy import Skype
from skpy import SkypeEventLoop, SkypeNewMessageEvent
import json

arq = open('/home/iqnus/passwords.json', 'rb')
texto = arq.read()
texto = json.loads(texto)
username = texto['skype']['username']
password = texto['skype']['password']

class SkypePing(SkypeEventLoop):
    def __init__(self):
        super(SkypePing, self).__init__(username, password)
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) \
          and not event.msg.userId == self.userId \
          and "ping" in event.msg.content:
            event.msg.chat.sendMsg("Pong!")
        print(event.msg.content)


skype_server = SkypePing()
skype_server.loop()
#ch = sk.chats.create(["joe.4", "daisy.5"]) # new group conversation
#ch = sk.contacts["joe.4"].chat # 1-to-1 conversation

#ch.sendMsg('content') # plain-text message
#ch.sendFile(open("song.mp3", "rb"), "song.mp3") # file upload
#ch.sendContact(sk.contacts["daisy.5"]) # contact sharing
sk.getMsgs()