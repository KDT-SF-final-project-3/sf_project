import serial
import pymysql

# 시리얼 포트 설정
ser = serial.Serial('COM5', 9600)

# MySQL 연결
conn = pymysql.connect(host='localhost', user='root', password='1111', db='Sensor')
cursor = conn.cursor()
  
while True:
    line = ser.readline().decode().strip()  # 예: "24.5,60.0"
    try:
        temp, hum = map(float, line.split(','))
        sql = "INSERT INTO dht_data (temperature, humidity) VALUES (%s, %s)"
        cursor.execute(sql, (temp, hum))
        conn.commit()
        print(f"Saved: Temp={temp}°C, Humidity={hum}%")
    except Exception as e:
        print("Error:", e)
