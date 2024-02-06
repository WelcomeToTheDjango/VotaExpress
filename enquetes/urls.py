# This file is used to register the urls of the enquetes app

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
]
