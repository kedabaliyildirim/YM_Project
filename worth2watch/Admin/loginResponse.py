
from django.http import JsonResponse


def adminLoginResponse(payload):
    print(payload)
    return JsonResponse({'status': 'ok'}, safe=False)