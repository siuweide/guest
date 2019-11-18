from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        # if username == 'admin' and password == 'admin123456':
        if user is not None:
            auth.login(request,user)
            request.session['user'] = username # 将session记录到浏览器
            response =  redirect('/project/event_manage/')
            return response
        else:
            error = 'username or password error'
            return render(request,'index.html',{'error':error})
    return render(request,'index.html')
