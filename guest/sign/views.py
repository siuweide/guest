from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from sign.models import Event, Guest

# Create your views here.

# 发布会管理
@login_required
def event_manage(request):
    events = Event.objects.all()
    return render(request,'event_manage.html',{
        'events':events
    })

# 发布会名称搜索
@login_required
def search_event_name(request):
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {
        'events':event_list
    })

# 嘉宾管理
def guest_manage(request):
    guests_list = Guest.objects.all()
    paginator = Paginator(guests_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html',{
        'guests':contacts
    })

# 嘉宾搜索
@login_required
def search_guest_name(request):
    search_name = request.GET.get('name', '')
    guest_list = Guest.objects.filter(realname__contains=search_name)
    return render(request, 'guest_manage.html', {
        'guests':guest_list
    })

# 签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event, id=eid)
    guest = Guest.objects.filter(event_id=eid).aggregate(realname=Count('realname'))
    guest_sign = Guest.objects.filter(event_id=eid, sign=True).aggregate(a=Count('realname'))['a'] #签到数
    guest_count = guest['realname']  #嘉宾数
    return render(request, 'sign_index.html',{
        'event':event,
        'guest_count':guest_count,
        'guest_sign':guest_sign
    })

# 签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    print('event----------------->',event)
    phone = request.POST.get('phone', '')
    print('phone------------------>',phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',{
            'event':event,
            'hint': 'phone error'})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html',{
            'event':event,
            'hint': 'event_id or phone error'})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if  result.sign:
        return render(request, 'sign_index.html',{
            'event':event,
            'hint': 'user has sign in '})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign="1")
        return render(request,  'sign_index.html', {
            'event':event,
            'hint': 'sign in success',
            'guest':result
        })