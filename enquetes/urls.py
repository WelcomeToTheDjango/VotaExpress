from django.urls import path
from . import views


urlpatterns = [
    path('enquetes', views.enquetes, name='enquetes')
]