import base64
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from bcrypt import hashpw, gensalt, checkpw

def admin_creation(payload):
    password = payload.get('password')
    email = payload.get('email')
    if password is not None and email is not None:
        password_bytes = password.encode('utf-8')
        password = hashpw(password_bytes, gensalt())
        collection('admin').insert_one({'email': email, 'password': password})
        return {'status': 'ok'}

def admin_list():
    docs = collection('admin').find({"email": {"$exists": True}})
    admin_list = []
    for doc in docs:
        admin_list.append(doc['email'])
    return admin_list

def admin_removal(payload):
    email = payload.get('email')
    if email is not None or email != '':
        currentAdmin = collection("admin").find_one({'auth_string.token': payload.get('authToken')})
        if currentAdmin['email'] != email:
            if collection('admin').find_one({'email': email}) is not None:
                if collection('admin').count_documents({}) == 1:
                    return {'status': 'error', 'message': 'You cannot remove the last admin'}
                else:
                    try:
                        collection('admin').delete_one({'email': email})
                        return {'status': 'ok'}
                    except Exception as e:
                        print("Delete Error:", e)
                        return {'status': 'error', 'message': 'Unexpected error'}
            else:
                return {'status': 'error', 'message': 'Admin not found'}
        else:
            return {'status': 'error', 'message': 'You cannot remove yourself'}
    else:
        return {'status': 'error', 'message': 'Admin not found'}
        
def admin_password_change(payload):
    email = payload.get('email')
    password = payload.get('password')
    authToken = payload.get('authToken')
    # if collection('admin').find({"authToken" : authToken})
    if collection('admin').find_one({'email': email}) is not None:
        if email is not None and password is not None:
            password_bytes = password.encode('utf-8')
            password = hashpw(password_bytes, gensalt())
            collection('admin').update_one({'email': email}, {'$set': {'password': password}})
            return {'status': 'ok'}
    else:
        return {'status': 'error', 'message': 'Admin not found'}