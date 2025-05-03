from django.urls import path
from .views import get_tables

urlpatterns = [
    path('get-tables/', get_tables),
]