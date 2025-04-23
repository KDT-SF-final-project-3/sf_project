from django.urls import path
from .views.RegisterView import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]