import time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from sign.models import Event,Guest


# 添加发布会接口
@csrf_exempt
def add_event(request):
    eid = request.POST.get('eid', '')                       # 发布会ID
    name = request.POST.get('name', '')                     # 发布会标题
    limit = request.POST.get('limit', '')                   # 限制人数
    status = request.POST.get('status', '')                 # 状态
    address = request.POST.get('address', '')               # 地址
    start_time = request.POST.get('start_time', '')         # 发布会时间

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status':10021, 'message':'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10022, 'message':'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status':10023, 'message':'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, status=status, address=address, start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS fromat'
        return JsonResponse({'status':10024, 'message':error})

    return JsonResponse({'status':200, 'message':'add event success'})


# 查询发布会接口
@login_required
def get_event(request):
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    print('eid----------->', eid)
    print('name----------->', name)
    if eid == '' and name == '':
        return JsonResponse({'status':10021, 'message':'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200, 'message':'success', 'data':event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        print('results:--------------------->',results)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200, 'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

# 添加嘉宾接口
@login_required
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status':10021, 'message':'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022, 'message':'event id is null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023, 'message':'event status is not available'})

    event_limit = Event.objects.get(id=eid).limit        # 发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)     # 发布会已添加的嘉宾数

    if len(guest_limit) >= event_limit:
        return JsonResponse({'status':10024, 'message':'event number is full'})

    event_time = Event.objects.get(id=eid).start_time    # 发布会时间
    etime = str(event_time).split("+")[0]
    e_time = time.mktime(time.strptime(etime, "%Y-%m-%d %H:%M:%S"))

    now_time = float(str(time.time()))                  # 当前时间

    if e_time > now_time:
        return JsonResponse({'status':10025,'message':'event has started'})
    try:
        Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'the event guest phone number repeat'})

    return JsonResponse({'status':200,'message':'add guest success'})

# 嘉宾查询接口
@login_required
def get_guest(request):
    eid = request.GET.get("eid", "")       # 关联发布会id
    phone = request.GET.get("phone", "")   # 嘉宾手机号

    if eid == '':
        return JsonResponse({'status':10021,'message':'eid cannot be empty'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone,event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status':200, 'message':'success', 'data':guest})

# 用户签到接口
@login_required
def user_sign(request):
    eid =  request.POST.get('eid','')       # 发布会id
    phone =  request.POST.get('phone','')   # 嘉宾手机号

    if eid =='' or phone == '':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time     # 发布会时间
    timeArray = time.strptime(str(event_time), "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())          # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status':10024,'message':'event has started'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status':10025,'message':'user phone null'})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return JsonResponse({'status':10026,'message':'user did not participate in the conference'})

    result = Guest.objects.get(event_id=eid,phone=phone).sign
    if result:
        return JsonResponse({'status':10027,'message':'user has sign in'})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return JsonResponse({'status':200,'message':'sign success'})

@login_required
def get_event_list(request):
    data = []
    if request.method == "GET":
        event_list = Event.objects.all()
        for event in event_list:
            events = {}
            events['id'] = event.id
            events['name'] = event.name
            events['limit'] = event.limit
            data.append(events)
        return JsonResponse({'status':200, 'message':'success', 'data':data})
    else:
        return JsonResponse({'status':10201, 'message':'request method error'})

@login_required
def cancel_event(request):
    if request.method == "POST":
        event_id = int(request.POST.get('event_id', ''))

        if event_id == '':
            return JsonResponse({'status': 10201, 'message': 'event_id is not null'})

        event_ids = []
        obj_event = Event.objects.all()
        for name in obj_event:
            event_ids.append(name.id)
        if event_id not in event_ids:
            return JsonResponse({'status': 10202, 'message': 'event_id is not exists'})

        event = Event.objects.get(id=event_id)
        event.delete()
        return JsonResponse({'status': 200, 'message': 'success'})

    else:
        return JsonResponse({'status':10203, 'message':'request method error'})

