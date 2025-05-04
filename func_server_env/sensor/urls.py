# sensor/urls.py
from django.urls import path
from .views import export_sensor_data

urlpatterns = [
    path('table3/export/', export_sensor_data),  # CSV 내보내기 엔드포인트
]
python
복사
편집
