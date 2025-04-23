from django.urls import path, include
from . import views

urlpatterns = [
    path('api/data/', views.get_data, name='get_data'),
]
