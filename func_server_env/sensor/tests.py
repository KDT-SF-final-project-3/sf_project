import requests

data = {
    "light": 111,
    "temperature": 22.5,
    "humidity": 44.0,
    "fan_status": "ON",
    "led_status": "OFF"
}

try:
    res = requests.post("http://127.0.0.1:8002/api/sensor/", json=data, timeout=3)
    print("✅ 응답 코드:", res.status_code)
    print("✅ 응답 내용:", res.text)
except Exception as e:
    print("❌ 요청 실패:", e)