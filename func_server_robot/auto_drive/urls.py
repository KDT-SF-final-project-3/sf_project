# auto_drive/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('manual_drive/control/', views.control_command),
]