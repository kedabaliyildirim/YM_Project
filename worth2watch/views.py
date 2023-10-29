import json
from django.http import JsonResponse
from worth2watch.Database.admin.adminLogins import isAuth
from worth2watch.Users.Admin.loginResponse import adminLoginResponse
from worth2watch.Database.content.DatabaseRequests import getData
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def index(request):
    document = getData()
    return JsonResponse(document, safe=False)


def getMovie(request, payload):
    print(payload)

@csrf_exempt
@require_POST
def getAuth(request):
    # payload = json.loads(request.body.decode('utf-8'))
    if isAuth(request.body.decode('utf-8')):
        return JsonResponse({'status': 'ok'})
    else: 
        return JsonResponse({'status': 'not authorized'})

@csrf_exempt
@require_POST
def logInAdmin(request):
    payload = json.loads(request.body.decode('utf-8'))
    isAuth = adminLoginResponse(payload)
    if isAuth['status'] == 'ok' and isAuth['authToken'] is not None:
        return JsonResponse({'status': 'ok', 'authToken': isAuth['authToken']})
    else:
        return JsonResponse({'status': 'wrong password'})
