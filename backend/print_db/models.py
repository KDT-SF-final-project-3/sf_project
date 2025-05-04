# models.py
from django.db import models

class Table3View(models.Model):
    id = models.BigAutoField(primary_key=True)
    light = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    fan_status = models.CharField(max_length=10)
    led_status = models.CharField(max_length=10)
    timestamp = models.CharField(max_length=24)  # varchar이므로 CharField

    class Meta:
        managed = False  # 뷰이기 때문에 마이그레이션 안 함
        db_table = 'table3'

class Table4(models.Model):
    id = models.BigAutoField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.CharField(max_length=24)
    end_time = models.CharField(max_length=24)

    class Meta:
        managed = False  # 뷰이기 때문에 마이그레이션 X
        db_table = 'table4'  # 뷰 이름

from django.db import models

class Table5(models.Model):
    id = models.BigIntegerField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.CharField(max_length=24)
    end_time = models.CharField(max_length=24)

    class Meta:
        managed = False  # ❗ DB View이므로 Django가 테이블 생성/삭제 X
        db_table = 'table5'


class Table7(models.Model):
    id = models.BigAutoField(primary_key=True)
    light = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    fan_status = models.CharField(max_length=10)
    led_status = models.CharField(max_length=10)
    timestamp = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'table7'