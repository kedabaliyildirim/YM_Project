import django
from django.http import JsonResponse
from worth2watch.Database.DatabaseRequests import getData
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.middleware.csrf import get_token


def index(request):
    document = getData()
    return JsonResponse(document, safe=False)


def getMovie(request, payload):
    print(payload)


@csrf_exempt
def logInAdmin(request, payload):
    print(payload)
    return JsonResponse({'status': 'ok'}, safe=False)


def get_csrf_token(request):
    print("@csrftoken")
    return JsonResponse({'csrfToken': get_token(request)})
