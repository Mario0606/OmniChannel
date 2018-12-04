from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = 'NAK0slzNmfeT7ZOiC2CW40jUQ'
CONSUMER_SECRET = 'AkWgYk3zRXrmoj9wQIkCyanGEywamU6IHobR28D4NA5CS4AQlL'
ACCESS_TOKEN = '4693049767-Zyt4hmyIrNnaHVlZZUMokF1C9uCEdoJ2WRUWFav'
ACCESS_SECRET = 'NuEq2v8RWgJxgOAFjEhjtxcpwoHLG8EVc8haPMBryZxKC'

ENVNAME = "prod"

def subscribe_account():
    CONSUMER_KEY = 'NAK0slzNmfeT7ZOiC2CW40jUQ'
    CONSUMER_SECRET = 'AkWgYk3zRXrmoj9wQIkCyanGEywamU6IHobR28D4NA5CS4AQlL'
    ACCESS_TOKEN = '4693049767-Zyt4hmyIrNnaHVlZZUMokF1C9uCEdoJ2WRUWFav'
    ACCESS_SECRET = 'NuEq2v8RWgJxgOAFjEhjtxcpwoHLG8EVc8haPMBryZxKC'

    ENVNAME = "prod"
    twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    r = twitterAPI.request('account_activity/all/:%s/subscriptions' %
                        ENVNAME, None, None, "POST")

    #TODO: check possible status codes and convert to nice messages
    print (r.status_code)
        
