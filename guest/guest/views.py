from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username=========',username)
        print('password=========',password)
        if username == '' or password == '':
            return render(request, 'index.html', {'error':'username or password is null'})

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            print('-----------------user is not none--------------------')
            auth.login(request,user)
            response =  redirect('/project/event_manage/')
            return response
        else:
            error = 'username or password error'
            return render(request,'index.html',{'error':error})
    return render(request,'index.html')

@login_required
def logout_action(request):
    auth.logout(request)
    response =  redirect('/login_action/')
    return response