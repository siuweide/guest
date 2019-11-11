from django.urls import path
from . import views

urlpatterns = [
    path('event_manage/', views.event_manage)
]