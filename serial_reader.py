import serial
import requests
import time

ser = serial.Serial('COM4', 9600, timeout=2)  # 포트 번호는 환경에 맞게 조정
url = 'http://127.0.0.1:8000/api/sensor/'

# 변수 초기화
light = None
temperature = None
humidity = None
fan_status = None
led_status = None

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        print("[시리얼 수신] ", line)

        if line.startswith("조도 값"):
            light = int(line.split(":")[1].strip())

        elif "습도" in line:
            humidity = float(line.split(":")[1].replace('%', '').strip())

        elif "온도" in line:
            temperature = float(line.split(":")[1].replace('°C', '').strip())

        elif "팬 모터" in line:
            fan_status = "ON" if "작동" in line else "OFF"

        elif "LED" in line:
            led_status = "ON" if "켜짐" in line else "OFF"

        # 디버깅 출력
        print("현재 상태:", light, temperature, humidity, fan_status, led_status)

        # 모든 값이 준비되었을 때 전송
        if None not in (light, temperature, humidity, fan_status, led_status):
            print(">>> 모든 값 준비 완료. 서버로 전송 중...")
            data = {
                'light': light,
                'temperature': temperature,
                'humidity': humidity,
                'fan_status': fan_status,
                'led_status': led_status
            }
        
            response = requests.post(url, json=data)
            print(">>> 전송 성공:", response.status_code, response.text)
        
            # 초기화
            light = temperature = humidity = fan_status = led_status = None

        time.sleep(0.2)

    except Exception as e:
        print("에러:", e)
        time.sleep(1)