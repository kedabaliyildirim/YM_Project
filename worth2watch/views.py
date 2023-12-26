import json
from django.http import JsonResponse
from worth2watch.Database.admin.adminLogins import isAuth
from worth2watch.Users.Admin.loginResponse import adminLoginResponse

from worth2watch.Database.content.DatabaseRequests import acquire_top_ten, getPaginatedData, getRequestedMovie, getSearchedMovie, totalPages
from worth2watch.Database.admin.admin_IO import admin_creation, admin_list, admin_removal, admin_password_change
from worth2watch.Database.content.content_csv_creator import create_csv_from_database
from worth2watch.Database.content.DataAcquisition import accquireData
from worth2watch.Database.content.database_removal import removeData
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from worth2watch.agent_main.agent_main import agent_movie_caller
from django.http import JsonResponse

from worth2watch.agent_main.agent_main import agent_movie_caller


@csrf_exempt
@require_POST
def index(request):
    payload = json.loads(request.body.decode('utf-8'))
    page = payload.get('page', 1)
    page_size = payload.get('page_size', 20)
    sort_by = payload.get('sort_by', 'movieName')
    sort_order = payload.get('sort_order', -1)
    document = getPaginatedData(page, page_size, sort_by, sort_order)
    return JsonResponse(document, safe=False)


def total_pages(request):
    page_size = int(request.GET.get('page_size', 20))
    document = totalPages(page_size)
    return JsonResponse(document, safe=False)


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


@csrf_exempt
@require_POST
def register_admin(request):
    payload = json.loads(request.body.decode('utf-8'))
    if isAuth(payload.get('authToken')):
        if admin_creation(payload)['status'] == 'ok':
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'unexpected error'})
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
def get_admin_list(request):
    if isAuth(request.body.decode('utf-8')):
        ad_list = admin_list()
        return JsonResponse(ad_list, safe=False)
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
@require_POST
def change_admin_password(request):
    payload = json.loads(request.body.decode('utf-8'))
    if isAuth(payload.get('authToken')):
        if admin_password_change(payload)['status'] == 'ok':
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'unexpected error'})
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
@require_POST
def remove_admin(request):
    payload = json.loads(request.body.decode('utf-8'))
    if isAuth(payload.get('authToken')):
        if admin_removal(payload)['status'] == 'ok':
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'unexpected error'})
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
@require_POST
def get_requested_movie(request):
    payload = json.loads(request.body.decode('utf-8'))
    moviePOBJ = getRequestedMovie(payload)
    if getRequestedMovie(payload) is not None:
        return JsonResponse(moviePOBJ, safe=False)
    else:
        return JsonResponse({'status': 'not found'})


@csrf_exempt
@require_POST
def get_searched_movie(request):
    payload = json.loads(request.body.decode('utf-8'))
    movieObj = getSearchedMovie(payload)
    if movieObj is not None:
        return JsonResponse(movieObj, safe=False)
    else:
        return JsonResponse({'status': 'not found'})


@csrf_exempt
@require_POST
def pull_content(request):
    payload = json.loads(request.body.decode('utf-8'))

    # Check if the request is authorized
    if isAuth(payload.get('authToken')):
        start_year = int(payload.get('startYear'))
        end_year = int(payload.get('endYear'))
        # Use range to iterate through years in intervals of 5
        for year in range(start_year, end_year + 1, 1):
            if year % 3 == 0:
                print(f"Pulling content for {year}...")
                accquireData(year)

        create_csv_from_database()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
@require_POST
def drop_database(request):
    payload = json.loads(request.body.decode('utf-8'))
    if isAuth(payload):
        removeData()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'not authorized'})


@csrf_exempt
def create_csv(request):
    print("@create_csv")
    create_csv_from_database()
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def get_top_ten(request):
    print("@get_top_ten")
    top_ten = acquire_top_ten()
    return JsonResponse(top_ten, safe=False)


@csrf_exempt
@require_POST
def pull_comments(request):
    payload = json.loads(request.body.decode('utf-8'))
    if isAuth(payload.get('authToken')):
        is_reddit = payload.get('platform') == 'reddit'
        is_youtube = payload.get('platform') == 'youtube'
        agent_movie_caller(reddit_status=is_reddit, youtube_status=is_youtube)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'not authorized'})
