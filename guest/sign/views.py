from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


def event_manage(request):
    return render(request,'event_manage.html')