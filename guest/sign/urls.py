from django.urls import path
from . import views
from . import views_if


urlpatterns = [
    # 发布会管理
    path('event_manage/', views.event_manage),
    # 发布会搜索
    path('search_event_name/', views.search_event_name),
    #嘉宾管理
    path('guest_manage/', views.guest_manage),
    # 嘉宾搜索
    path('search_guest_name/', views.search_guest_name),
    # 签到
    path('sign_index/<int:eid>/', views.sign_index),
    #  签到动作
    path('sign_index_action/<int:eid>/', views.sign_index_action),

    # 添加发布会接口地址
    path('add_event/', views_if.add_event),
    path('add_guest/', views_if.add_guest),
    path('get_event/', views_if.get_event),
    path('get_guest/', views_if.get_guest),
    path('get_event_list/', views_if.get_event_list),
    path('cancel_event/', views_if.cancel_event),
]