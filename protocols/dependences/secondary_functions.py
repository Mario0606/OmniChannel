def payload_send_DM_facebook(id,text):
    payload = {'recipient': {'id': id}, 'message': {'text':text}}
    return payload