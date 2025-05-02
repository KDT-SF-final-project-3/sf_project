from django.urls import path
from .views import sensor_data

urlpatterns = [
    path('sensor/', sensor_data),
]