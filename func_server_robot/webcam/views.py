# webcam/views.py

from django.http import StreamingHttpResponse
import cv2
from ultralytics import YOLO  # <-- YOLOv8 불러오기
import torch

# YOLO 모델 로딩 (가장 작은 모델 yolov8n.pt 사용)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO('yolov8n.pt').to(device)

def generate_camera_stream():
    cap = cv2.VideoCapture(0)  # 0번 웹캠
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임을 YOLOv8 모델에 넣어서 탐지
        results = model.predict(frame, imgsz=640, conf=0.5, verbose=False)

        # 탐지된 결과를 프레임에 그리기
        annotated_frame = results[0].plot()  # bounding box 그리기

        # 프레임을 JPEG로 인코딩
        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = jpeg.tobytes()

        # 스트리밍
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(generate_camera_stream(),
                                  content_type='multipart/x-mixed-replace; boundary=frame')