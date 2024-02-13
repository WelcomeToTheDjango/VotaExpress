# This file is used to handle the requests of the enquetes app

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings


@login_required(login_url=settings.LOGIN_URL)
def home(request):
    return render(request, "enquetes/home.html")
