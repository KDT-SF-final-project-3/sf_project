import serial
import requests
import time

ser = serial.Serial('COM4', 9600, timeout=2)  # 환경에 맞게 포트 확인
url = 'http://127.0.0.1:8002/api/sensor/'     # 서버 포트 확인

sensor_data = {}

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        print("[시리얼 수신]", line)

        if "조도 값" in line:
            sensor_data['light'] = int(line.split(":")[1].strip())

        elif "습도" in line:
            sensor_data['humidity'] = float(line.split(":")[1].replace('%', '').strip())

        elif "온도" in line:
            sensor_data['temperature'] = float(line.split(":")[1].replace('°C', '').strip())

        elif "팬 모터" in line:
            sensor_data['fan_status'] = "ON" if "작동" in line else "OFF"

        elif "LED" in line:
            sensor_data['led_status'] = "ON" if "켜짐" in line else "OFF"

        print("현재 누적된 센서 값 수:", len(sensor_data), "/ 5")

        if len(sensor_data) == 5:
            print("✅ 전송할 데이터:", sensor_data)
            response = requests.post(url, json=sensor_data, timeout=3)
            print(">>> 응답:", response.status_code, response.text)
            sensor_data.clear()

        time.sleep(0.2)

    except Exception as e:
        print("❌ 에러 발생:", e)
        time.sleep(1)