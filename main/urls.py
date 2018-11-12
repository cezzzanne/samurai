from django.urls import path, include
from .views import register, custom_login, home, main, create_group, join_group

urlpatterns = [
    path('', register),
    path('login', custom_login),
    path('home', home),
    path('create-group', create_group),
    path('join-group/<group_id>', join_group),
    path('main', main)
]
