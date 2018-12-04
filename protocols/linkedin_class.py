from linkedin_v2 import linkedin
from flask import Flask, request
from PyLinkedinAPI.PyLinkedinAPI import PyLinkedinAPI 
import requests
import json
import traceback
import os
API_KEY = '77mosx338k3ts1'
API_SECRET = '7I5IfCS0MUe40WIZ'
RETURN_URL = 'https://237920fe.ngrok.io/linkedin'
SCOPE = "r_emailaddress%20w_share?rw_company_admin"
access_token = 'AQXXZ1qv2ZavsrPDxz3AGTKvMYA-n9S5z_WaLlWWIZvy0MxhzMxXht3J6Z2lyHkSOkyKcjFxi2zQlsjDESO7eRsEv5qcKCYqYdibpaNE7SBZA-buEhTKxhr8N33LwtPp8YPH6gVLa39BsoE6NxW6WUjho0jIjDsAzeOIJ2AXj9Ow8yc0S3UdLhQmnM-HnsapV4AeCJN46lK4P4Rrtg9AGMh3hssL70rnhXj9t1bPm2IrJh3YhQ4nY4DwbZs1lDeuj6Zg6TQIcFTGUJ9lxPnAcxfPwVggf4HbXaRS0xj1THS6OUMelk8-3lLeIrGX7Jd8348Dpr7jbcC6d4V-i8Vns1LnZchKGA'
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL)


app = Flask(__name__)
linkedin1 = PyLinkedinAPI(access_token)
if(__name__ == '__main__'):
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())

    print(authentication.authorization_url)  # open this url on your browser
    application = linkedin.LinkedInApplication(authentication)
    app.run(debug=True)
    
@app.route('/linkedin', methods=['POST'])
def linkedin_request():   
    if request.method == 'POST':
        try:
            data1 = request.data.decode()
            print(data1)
            data = json.loads(request.data.decode())
            print(data)
            
        except:
            print(traceback.format_exc())
    
    elif request.method == 'GET':               
        if request.args.get('MessageBotTest') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"      