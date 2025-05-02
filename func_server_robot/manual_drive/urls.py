from django.urls import path
from . import views

urlpatterns = [
    path('control/', views.control_arduino, name='control_arduino'),
]