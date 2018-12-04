#wrong
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
from protocol_class import protocol
import traceback
import requests
from queue import Queue
from threading import Thread, Event
import os
import base64
from dependences.gmail_methods import ListHistory,GetMessage,GetMimeMessage
from dependences.gmail_methods import CreateMessageWithAttachment,send_mail
from protocol_class import protocol
from time import sleep
#from google.cloud import pubsub_v1

class gmail(Thread):
    def __init__(self):
        super().__init__()
        self._iqueue = Queue()
        self._oqueue = None
        self._qaux = None
        self._alive = Event()
        self._service = None
 
    #def topic(self,topic_name,subscription_name,endpoint):
    #    publisher = pubsub_v1.PublisherClient()
    #    topic_path = publisher.api.topic_path('emailbot-221318', topic_name)
    #    project_path = publisher.api.project_path("emailbot-221318")
    #    if (topic_name not in project_path):     
    #        topic = publisher.api.create_topic(topic_path)
    #        print('Topic created: {}'.format(topic))
#
    #    subscriber = pubsub_v1.SubscriberClient()
    #    topic_path = subscriber.api.topic_path('emailbot-221318', topic_name)
    #    subscription_path = subscriber.api.subscription_path(
    #        'project_id', subscription_name)
#
    #    push_config = pubsub_v1.subscriber.types.PushConfig(
    #        push_endpoint=endpoint)
#
    #    subscription = subscriber.api.create_subscription(
    #        subscription_path, topic_path, push_config)

    def auth(self):
        SCOPES = ['https://mail.google.com','https://www.googleapis.com/auth/pubsub',
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/gmail.readonly']

        store = file.Storage('/home/iqnus/Documentos/omnichannel/src/jsons/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('/home/iqnus/Documentos/omnichannel/src/jsons/client_token.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self._service = build('gmail', 'v1', http=creds.authorize(Http()))

    def process_msg(self,data):
        text = data['message']['data']
        msgId = data['message']['message_id']
        text = base64.urlsafe_b64decode(text)
        text = str(text)
        text = text.split("'")[1]
        text = json.loads(text)
        email_address = text['emailAddress']
        historyId = text['historyId']
        start_id = int(historyId) -60
        msgId = ListHistory(self._service,start_id)
        try:
            json_msg = GetMessage(self._service,"me",msgId)
        except:
            print(traceback.format_exc())
        if(json_msg['labelIds'][0] == 'SENT'):
            return None
        tittle = json_msg['payload']['headers'][19]['value']
        body = json_msg['snippet']
        msg_text = "Tittle: "+tittle+"        "+"Text: "+body
        id = json_msg['payload']['headers'][16]['value']
        id = id.split("\u003c")[1]
        id = id.split("\u003e")[0]
        gmail_object = protocol("Gmail","E-mail",id,id,msg_text,"")
        return gmail_object

    def send_email(self,msg_obj):
        message = CreateMessageWithAttachment("me",msg_obj.id,"test",msg_obj.text,"image.jpg")
        send_mail(self._service,"me",message)

    def run(self):
        print("blabla")
        self.auth()
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
                self.send_email(msg_obj)
