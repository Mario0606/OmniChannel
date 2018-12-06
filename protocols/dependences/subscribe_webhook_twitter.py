from TwitterAPI import TwitterAPI
import json
import os

arq = open('/home/iqnus/passwords.json', 'rb')
text = arq.read()
text = json.loads(text)

def subscribe_webhook(API,ENVNAME):
    r = API.request('account_activity/all/:%s/subscriptions' %
                           ENVNAME, None, None, "POST")
    #TODO: check possible status codes and convert to nice messages
    print (r.status_code)
       
