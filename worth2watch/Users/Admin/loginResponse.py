
from django.http import JsonResponse
from bcrypt import hashpw, gensalt, checkpw
from bson import json_util
from worth2watch.Database.admin.adminLogins import logInAdmin


import json
def adminLoginResponse(payload):
    admin = logInAdmin(payload['email'])
    
    if admin['status'] == 'user not found':
        return {'status': 'user not found'}
    else:
        admin_dict = admin['user']

    passStatus = checkpw(payload['password'].encode('utf-8'), admin_dict['password'])
    
    if passStatus:
        return {'status': 'ok','authToken': admin['authToken']}
    else:
        return {'status': 'wrong password'}
