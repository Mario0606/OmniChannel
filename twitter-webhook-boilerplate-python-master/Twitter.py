from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = 'NAK0slzNmfeT7ZOiC2CW40jUQ'
CONSUMER_SECRET = 'AkWgYk3zRXrmoj9wQIkCyanGEywamU6IHobR28D4NA5CS4AQlL'
ACCESS_TOKEN = '4693049767-Zyt4hmyIrNnaHVlZZUMokF1C9uCEdoJ2WRUWFav'
ACCESS_SECRET = 'NuEq2v8RWgJxgOAFjEhjtxcpwoHLG8EVc8haPMBryZxKC'


def initApiObject():
    
    #user authentication
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)    
    
    return api				
 
def processDirectMessageEvent(eventObj):
    
    messageText = eventObj.get('message_data').get('text')
    userID = eventObj.get('sender_id')

    twitterAPI = initApiObject()
            
    messageReplyJson = '{"event":{"type":"message_create","message_create":{"target":{"recipient_id":"' + userID + '"},"message_data":{"text":"Hello World!"}}}}'
        
    #ignore casing
    if(messageText.lower() == 'hello bot'):
            
        r = twitterAPI.request('direct_messages/events/new', messageReplyJson)
          
    return None      

def processLikeEvent(eventObj):
    userHandle = eventObj.get('user', {}).get('screen_name')
    
    print ('This user liked one of your tweets: %s' % userHandle) 
    
    return None           
