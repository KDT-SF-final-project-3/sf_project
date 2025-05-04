# auto_drive/detector_thread.py

import cv2
import numpy as np
import time
import serial
from .views import active_state  # 전역 상태 가져오기

def get_color_from_hsv(h, s, v):
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

def send_command(ser, cmd):
    print(f"[전송] {cmd}")
    ser.write((cmd + "\n").encode())
    time.sleep(1.5)

def run_detector():
    ser = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    ser.write(b"a\n")

    config_path = "yolov4-tiny.cfg"
    weights_path = "yolov4-tiny.weights"
    names_path = "coco.names"

    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(weights_path, config_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    cap = cv2.VideoCapture(0)
    processing = False

    while True:
        if not active_state["is_active"]:
            time.sleep(1)
            continue

        ret, frame = cap.read()
        if not ret:
            break

        # YOLO 병 감지 로직 그대로 붙여넣기
        # [중략] 기존 YOLO 병 + 색상 판단 코드 사용

    cap.release()
    cv2.destroyAllWindows()
    ser.close()