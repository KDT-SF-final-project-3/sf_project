from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from .serial_handler import send_to_arduino
from .models import CommandLog
import time

def control_arduino(request):
    command = request.GET.get('cmd')
    if not command:
        return JsonResponse({'status': 'error', 'message': '명령이 없습니다.'}, status=400)

    try:
        start_time = timezone.now()
        log = CommandLog.objects.create(command=command, start_time=start_time)

        send_to_arduino(command)
        time.sleep(1)  # 약간의 딜레이 고려

        log.end_time = timezone.now()
        log.save()

        return JsonResponse({'status': 'ok', 'command': command})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# 로그 확인용 (선택)
def get_logs(request):
    logs = CommandLog.objects.order_by('-start_time')[:20]
    data = [
        {
            'command': log.command,
            'start_time': log.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': log.end_time.strftime('%Y-%m-%d %H:%M:%S') if log.end_time else None,
        }
        for log in logs
    ]
    return JsonResponse({'logs': data})