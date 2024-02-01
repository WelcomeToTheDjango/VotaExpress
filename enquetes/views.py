# This file is used to handle the requests of the enquetes app

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")
