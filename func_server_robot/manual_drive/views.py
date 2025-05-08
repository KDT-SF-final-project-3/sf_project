from django.http import JsonResponse
from django.utils import timezone
from .models import CommandLog, AutoLog
from .serial_handler import send_to_arduino
import threading
import cv2
import numpy as np
import time
from ultralytics import YOLO
from webcam.views import cap

auto_mode = {"active": False}

def detect_color(h, s, v):
    if v < 40:
        return "black"
    elif s < 30 and v > 200:
        return "white"
    elif s < 40:
        return "gray"
    elif h < 10 or h >= 160:
        return "red"
    elif 35 <= h < 85:
        return "green"
    elif 85 <= h < 110:
        return "blue"
    else:
        return "other"

def start_auto_detection():
    model = YOLO("yolov8n.pt")
    detection_cooldown = 3
    last_detection_time = 0

    while auto_mode["active"]:
        ret, frame = cap.read()
        if not ret:
            continue

        if time.time() - last_detection_time < detection_cooldown:
            time.sleep(0.1)
            continue

        results = model(frame, verbose=False)
        detected = False

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if conf < 0.3:
                    continue

                label = model.names[cls]
                if label != "bottle":
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                roi = frame[y1:y2, x1:x2]
                if roi.size == 0:
                    continue

                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                h_mean = hsv[:, :, 0].mean()
                s_mean = hsv[:, :, 1].mean()
                v_mean = hsv[:, :, 2].mean()
                color = detect_color(h_mean, s_mean, v_mean)

                print(f"인식 색상: {color}")

                # 시작 시간 기록
                start_time = timezone.now()

                # 색상별 명령 처리
                if color == "red":
                    send_to_arduino("1,d,-8")
                    send_to_arduino("3,a,80")
                    send_to_arduino("2,d,-6")
                    send_to_arduino("1,d,8")
                    time.sleep(3)
                    send_to_arduino("2,d,10")
                    send_to_arduino("3,a,-80")
                    send_to_arduino("2,d,-3")
                elif color == "blue":
                    send_to_arduino("1,d,-8")
                    send_to_arduino("3,a,-80")
                    send_to_arduino("2,d,-6")
                    send_to_arduino("1,d,8")
                    time.sleep(3)
                    send_to_arduino("2,d,10")
                    send_to_arduino("3,a,80")
                    send_to_arduino("2,d,-3")
                elif color == "green":
                    send_to_arduino("1,d,-8")
                    send_to_arduino("3,a,-180")
                    send_to_arduino("2,d,-11")
                    send_to_arduino("1,d,8")
                    time.sleep(3)
                    send_to_arduino("2,d,15")
                    send_to_arduino("3,a,180")
                    send_to_arduino("2,d,-3")
                else:
                    print("[무시] 색상:", color)

                # 종료 시간 기록 및 로그 저장
                end_time = timezone.now()
                AutoLog.objects.create(
                    command=f"{color} 병 감지",
                    start_time=start_time,
                    end_time=end_time
                )

                last_detection_time = time.time()
                detected = True
                break
            if detected:
                break

        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

def control_arduino(request):
    command = request.GET.get("cmd")
    now = timezone.now()

    if not command:
        return JsonResponse({'status': 'error', 'message': '명령 없음'}, status=400)

    try:
        command_map = {
            '잡기': '1,2', '놓기': '1,1', '상승': '2,1', '하강': '2,2',
            '회전': '3,1', '역회전': '3,2', '수동': 'm', '자동': 'a', '정지': 'q'
        }
        command_str = command_map.get(command, command)

        if command_str == 'a':
            if not auto_mode["active"]:
                auto_mode["active"] = True
                threading.Thread(target=start_auto_detection, daemon=True).start()
                print("🚗 자동 모드 시작됨")
            send_to_arduino('a')

        elif command_str == 'm':
            auto_mode["active"] = False
            print("🛑 수동 모드 전환됨")
            send_to_arduino('m')

        elif command_str == 'q':
            # 마지막으로 실행된 명령 중 end_time이 비어 있는 것만 종료 처리
            CommandLog.objects.filter(end_time__isnull=True).update(end_time=now)
            send_to_arduino('q')
            return JsonResponse({'status': 'ok', 'message': '정지 명령 실행됨'})

        else:
            # 수동 명령 실행 로그 저장
            CommandLog.objects.create(command=command, start_time=now)
            send_to_arduino(command_str)

        return JsonResponse({'status': 'ok', 'message': f'{command} 실행됨'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)