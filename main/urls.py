from django.urls import path, include
from .views import test, test_success, register, custom_login, home, success

urlpatterns = [
    path('', test),
    path('register', register),
    path('login', custom_login),
    path('home', home),
    path('success', success)
]
