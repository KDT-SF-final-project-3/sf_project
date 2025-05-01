from django.db import models

class CommandLog(models.Model):
    command = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'manual_dirve'  # 👉 테이블명 지정 (MySQL에 생성될 이름)