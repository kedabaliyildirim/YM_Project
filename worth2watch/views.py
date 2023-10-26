# example/views.py
from django.http import JsonResponse
from worth2watch.Database.DatabaseRequests import getData
def index(request):
    document = getData()
    return JsonResponse(document, safe=False)