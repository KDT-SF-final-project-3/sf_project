# urls.py
from django.urls import path
from .views import Table3APIView
from .views import Table4APIView
from .views import Table7APIView


urlpatterns = [
    path('table3/', Table3APIView.as_view(), name='table3-api'),
    path('table4/', Table4APIView.as_view(), name='table4-api'),
    path('table7/', Table7APIView.as_view(), name='table7-api'),
]

