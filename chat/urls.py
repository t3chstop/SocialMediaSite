from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ws/<str:room_name>/', views.room, name='room'), #room name is actually the room pk
]