from django.urls import path
from . import views

urlpatterns = [
    path('control/', views.control_arduino, name='control_arduino'),
    path('logs/', views.get_logs, name='get_logs'),  # 선택적
]