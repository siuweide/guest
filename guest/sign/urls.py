from django.urls import path
from . import views

urlpatterns = [
    path('login_action/',views.login_action),
    path('event_manage/', views.event_manage)
]