from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == 'admin' and password == 'admin123456':
            return redirect('/project/event_manage/')
        else:
            error = 'username or password error'
            return render(request,'index.html',{'error':error})
    return HttpResponse('ok')


def event_manage(request):
    return render(request,'event_manage.html')