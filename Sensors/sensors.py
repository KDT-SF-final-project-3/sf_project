import serial
import pymysql
import time

# 시리얼 포트 설정
ser = serial.Serial('COM5', 9600, timeout=1)

# MySQL 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1111',
    db='Sensor_db',
    charset='utf8'
)
cursor = conn.cursor()

# 값 저장용 임시 변수
light = None
humidity = None
temperature = None

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("받은 데이터:", line)
            if "조도 값:" in line:
                light = int(line.replace("조도 값:", "").strip())
            elif "습도:" in line:
                humidity = float(line.replace("습도:", "").replace("%", "").strip())
            elif "온도:" in line:
                temperature = float(line.replace("온도:", "").replace("°C", "").strip())

                # 모든 값 수신 후 상태 판단 → DB 저장
                if temperature is not None and humidity is not None and light is not None:
                    # 팬 상태 판단
                    fan_status = "작동중" if humidity >= 70 else "꺼짐"

                    # LED 상태 판단
                    led_status = "켜짐" if light <= 60 else "꺼짐"

                    sql = """
                    INSERT INTO sensor (temperature, humidity, light, fan_status, led_status)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (temperature, humidity, light, fan_status, led_status))
                    conn.commit()

                    print(f"DB 저장됨 → 온도: {temperature}°C, 습도: {humidity}%, 조도: {light}")
                    print(f"팬 상태: {fan_status}, LED 상태: {led_status}")
                    print("---")

                    # 값 초기화
                    light = None
                    humidity = None
                    temperature = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("프로그램 종료 (Ctrl+C)")

finally:
    cursor.close()
    conn.close()
    ser.close()
    print("DB 및 시리얼 연결 종료됨.")
