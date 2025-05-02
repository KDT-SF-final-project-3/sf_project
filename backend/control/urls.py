from django.urls import path
from . import views

urlpatterns = [
    path('control/', views.proxy_command, name='proxy_command'),
]