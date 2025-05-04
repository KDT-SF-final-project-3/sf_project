# auto_drive/views.py

from django.http import JsonResponse

# 전역 플래그
active_state = {"is_active": False}

def control_command(request):
    cmd = request.GET.get('cmd', '')

    if cmd == 'a':
        active_state["is_active"] = True
        return JsonResponse({'status': '자동 인식 시작'})
    elif cmd == 'm':
        active_state["is_active"] = False
        return JsonResponse({'status': '자동 인식 중지'})
    else:
        return JsonResponse({'error': '잘못된 명령입니다'}, status=400)