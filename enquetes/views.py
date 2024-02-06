# This file is used to handle the requests of the enquetes app
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "enquetes/home.html")

def index(request):
    return HttpResponse("Hello World")
