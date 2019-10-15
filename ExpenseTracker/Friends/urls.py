from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('friends', views.index, name='friends'),
    path('leaderboards', views.index, name='leaderboards'),

 
]
