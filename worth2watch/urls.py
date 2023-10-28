# example/urls.py
from django.urls import path

from worth2watch.views import index, getMovie, logInAdmin, get_csrf_token
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('allmovies', index),
    path('movie/admin/addmovie', getMovie),
    path('admin/login', logInAdmin),
    path('auth', get_csrf_token),
]