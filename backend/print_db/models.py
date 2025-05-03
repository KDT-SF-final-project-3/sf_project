from django.db import models

class Table1(models.Model):
    id = models.BigAutoField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'table1'


class Table2(models.Model):
    id = models.BigAutoField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'table2'


class Table3(models.Model):
    id = models.BigAutoField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'table3'


class Table4(models.Model):
    id = models.BigAutoField(primary_key=True)
    command = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'table4'