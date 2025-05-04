# sensor/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import SensorData
import csv

@api_view(['GET'])
def export_sensor_data(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not (start and end):
        return Response({'error': '시작 및 종료 시간이 필요합니다.'}, status=400)

    data = SensorData.objects.filter(timestamp__range=[start, end]).order_by('timestamp')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensor_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', '조도', '온도', '습도', '팬 상태', 'LED 상태', '시간'])

    for item in data:
        writer.writerow([
            item.id,
            item.light,
            item.temperature,
            item.humidity,
            item.fan_status,
            item.led_status,
            item.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response