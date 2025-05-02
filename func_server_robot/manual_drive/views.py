from django.http import JsonResponse
from django.utils import timezone
from .models import CommandLog
from .serial_handler import send_to_arduino  # 시리얼 전송 함수

def control_arduino(request):
    command = request.GET.get('cmd')
    now = timezone.now()

    if not command:
        return JsonResponse({'status': 'error', 'message': '명령이 없습니다.'}, status=400)

    try:
        if command.lower() == 'q':
            # 🔹 q 명령 → 이전 명령 종료 처리만 하고, 본인은 로그에 안 남김
            CommandLog.objects.filter(end_time__isnull=True).update(end_time=now)
            send_to_arduino('q')
            return JsonResponse({'status': 'ok', 'message': '정지 명령 실행됨 (로그에는 저장 안 됨)'})

        # 🔹 일반 명령 → start_time 기록만 저장, end_time은 나중에 q로 처리
        CommandLog.objects.create(command=command, start_time=now)
        send_to_arduino(command)

        return JsonResponse({'status': 'ok', 'message': f'{command} 실행됨'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)