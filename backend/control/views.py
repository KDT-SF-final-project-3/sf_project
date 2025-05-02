from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_command(request):
    cmd = request.GET.get('cmd')
    if not cmd:
        return JsonResponse({'status': 'error', 'message': '명령이 없습니다.'}, status=400)

    try:
        response = requests.get('http://127.0.0.1:8001/manual_drive/control/', params={'cmd': cmd})
        return JsonResponse({'status': 'ok', 'from_backend': response.json()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)