"""
OmniChannel
"""
__version__ = '0.1'
__author__ = 'Iqnus'
#-*- coding: utf-8 -*-
from tweepy import OAuthHandler
from queue import Queue

from facebook_class import facebook
from gmail_class import gmail
from console_class import console
from twitter_class import twitter
from instagram_class import instagram

from flask import Flask, request,render_template
import json
import traceback
import os

#data of Twitter access 
arq = open('/home/iqnus/passwords.json', 'rb')
texto = arq.read()
texto = json.loads(texto)
ckey = texto['twitter']['ckey']
csecret = texto['twitter']['csecret']
atoken = texto['twitter']['atoken']
asecret = texto['twitter']['asecret']
print(atoken)
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
#data of Facebook access
page_token = texto['facebook']['page_token']


app = Flask(__name__)
qaux_F = Queue()
qaux_G = Queue()
qaux_I = Queue()



'''Flask Routes '''
#@app.route('/twitter', methods=['GET','POST'])
#def webhook_twitter():
#    if request.method == 'POST':
#        try:
#            data = json.loads(request.data.decode())
#            print(data)
#            return '200'
#        except:
#            print(traceback.format_exc())

@app.route('/gmail', methods=['GET', 'POST'])
def webhook_gmail():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_G.put(data)
            return "200"
            
        except:
            print(traceback.format_exc())

@app.route('/facebook', methods=['GET', 'POST'])
def webhook_facebook():      
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_F.put_nowait(data)
        except:
            print(traceback.format_exc())
    elif request.method == 'GET':                 
        if request.args.get('MessageBotTest') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"  

@app.route('/instagram', methods=['GET', 'POST'])
def webhook_instagram():      
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            qaux_I.put_nowait(data)
        except:
            print(traceback.format_exc())
    elif request.method == 'GET':                 
        if request.args.get('MessageBotTest') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing" 
@app.route("/googleddcf0dcf86bb8352.html/") 
def render(self):
    return render_template("googleddcf0dcf86bb8352.html")

@app.route('/auth-facebook')
def auth_facebook():
    if request.method == 'POST':
        data = json.loads(request.data.decode())
    elif request.method == 'GET':
        data = json.loads(request.data.decode())
    print(data)


if __name__=='__main__':
    
    twitter1 = twitter(auth)
    facebook1 = facebook(page_token)
    gmail1 = gmail() 
    instagram1 = instagram()
    console1 = console()

    console1._oqueue_t, twitter1._oqueue = twitter1._iqueue, console1._iqueue
    console1._oqueue_f, facebook1._oqueue = facebook1._iqueue, console1._iqueue
    console1._oqueue_g, gmail1._oqueue = gmail1._iqueue,console1._iqueue
    console1._oqueue_g, instagram1._oqueue = instagram1._iqueue,console1._iqueue

    facebook1._qaux = qaux_F
    gmail1._qaux = qaux_G
    instagram1._qaux = qaux_I

    gmail1.start()
    facebook1.start()
    twitter1.start()
    instagram1.start()
    console1.start()

    app.run(debug=True)
