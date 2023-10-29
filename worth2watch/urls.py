# example/urls.py
from django.urls import path

from worth2watch.views import index, getMovie, logInAdmin, getAuth
urlpatterns = [
    path('allmovies', index),
    path('movie/admin/addmovie', getMovie),
    path('mod/log', logInAdmin),
    path('getAuth', getAuth),
]
