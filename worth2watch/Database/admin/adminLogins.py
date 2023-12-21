import datetime
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
import base64


def isAuth(payload):
    authState = collection('admin').find_one({'auth_string.token': payload})
    checkExpiration = authState['auth_string']['auth_expiration_date'] > datetime.datetime.now(
    )
    if (checkExpiration):
        return True
    else:
        print('auth is not valid')
        collection('admin').update_one(
            {'auth_string.token': payload}, {'$unset': {'auth_string': ''}})
        return False
    # return True if authState is not None else False


def logInAdmin(payload):
    user = collection("admin").find_one({'email': payload})
    if user is None:
        return {'status': 'user not found'}
    else:
        authToken = create_basic_auth_string(user['email'], user['password'])
        if (authToken is not None):
            return {'status': 'ok', 'user': user, 'authToken': authToken}


def create_basic_auth_string(username, password):
    credentials = f"{username}: {password}"
    credentials_bytes = credentials.encode('utf-8')
    encoded_credentials = base64.b64encode(credentials_bytes).decode('utf-8')
    auth_string = {
        'token': encoded_credentials,
        'auth_expiration_date': datetime.datetime.now() + datetime.timedelta(days=1)
    }
    collection("admin").update_one({'email': username}, {
        '$set': {'auth_string': auth_string
                 }})
    return auth_string['token']
