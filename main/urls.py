from django.urls import path, include
from .views import test, test_success
urlpatterns = [
    path('', test),
    path('success', test_success)
]
