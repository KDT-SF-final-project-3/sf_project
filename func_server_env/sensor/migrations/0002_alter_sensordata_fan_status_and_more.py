# Generated by Django 5.2 on 2025-05-07 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensordata",
            name="fan_status",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="sensordata",
            name="humidity",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="sensordata",
            name="led_status",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="sensordata",
            name="light",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="sensordata",
            name="temperature",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
