import serial

# 실제 포트 확인 후 수정 (예: COM3 or /dev/ttyACM0)
ser = serial.Serial('COM5', 9600, timeout=1)

def send_to_arduino(command: str):
    ser.write((command + '\n').encode('utf-8'))
    print(f"[아두이노 전송됨]: {command}")
