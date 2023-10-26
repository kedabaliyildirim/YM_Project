# example/urls.py
from django.urls import path

from worth2watch.views import index


urlpatterns = [
    path('', index),
]