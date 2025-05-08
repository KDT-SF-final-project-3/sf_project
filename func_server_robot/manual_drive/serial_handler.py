# manual_drive/serial_handler.py
import serial

class ManualDriveSerial:
    def __init__(self):
        try:
            self.ser = serial.Serial('COM5', 9600, timeout=1)
            print("Manual drive serial connected.")
        except Exception as e:
            print("Failed to connect COM5:", e)
            self.ser = None

    def send(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())

manual_serial = ManualDriveSerial()

import time

def send_to_arduino(data):
    print(f"📡 아두이노로 전송됨: {data}")
    manual_serial.ser.write((data + "\n").encode())
    time.sleep(0.3)  # 🔹 명령 사이 딜레이로 안정성 확보