from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required
def event_manage(request):
    username = request.session.get('user','')  #读取浏览器的cookie
    print('名字是：',username)
    return render(request,'event_manage.html',{
        'user':username
    })