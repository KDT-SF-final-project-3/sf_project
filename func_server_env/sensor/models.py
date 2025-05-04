# sensor/models.py
from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField()
    light = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    fan_status = models.CharField(max_length=10, null=True, blank=True)
    led_status = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'sensor_data'