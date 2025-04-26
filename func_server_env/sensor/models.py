# sensor/models.py
from django.db import models

class SensorData(models.Model):
    light = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    fan_status = models.CharField(max_length=10)
    led_status = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sensor_data'  # 고정 테이블 이름!