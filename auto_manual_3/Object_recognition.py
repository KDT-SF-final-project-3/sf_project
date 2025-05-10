# ## 2초 후 인식 되는것

# import cv2
# import numpy as np
# import datetime
# import pymysql
# import time  # 로봇팔 동작 시 딜레이 주기 위함

# # DB 연결 설정
# conn = pymysql.connect(host='localhost', user='root', password='1234', db='sensor_db')
# cursor = conn.cursor()

# # YOLO 설정
# config_path = "yolov4-tiny.cfg"
# weights_path = "yolov4-tiny.weights"
# names_path = "coco.names"

# with open(names_path, "r") as f:
#     classes = [line.strip() for line in f.readlines()]

# net = cv2.dnn.readNet(weights_path, config_path)
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# # 색상 판별 함수
# def get_color_from_hsv(h, s, v):
#     if v < 40:
#         return "black"
#     elif s < 30 and v > 200:
#         return "white"
#     elif s < 40:
#         return "gray"
#     elif (h < 10 or h >= 160):
#         return "red"
#     elif 10 <= h < 25:
#         return "orange"
#     elif 25 <= h < 35:
#         return "yellow"
#     elif 35 <= h < 85:
#         return "green"
#     elif 85 <= h < 110:
#         return "blue"
#     elif 110 <= h < 135:
#         return "navy"
#     elif 135 <= h < 160:
#         return "purple"
#     else:
#         return "other"

# # 인식 중 여부 플래그
# processing = False

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("웹캠 열기 실패")
#     exit()

# # 2초 대기
# time.sleep(2)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     height, width = frame.shape[:2]

#     # YOLO 입력
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes = []
#     confidences = []
#     class_ids = []

#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]

#             if confidence > 0.2:
#                 label = classes[class_id]

#                 if label == "person":
#                     continue

#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)

#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)

#     if len(indexes) > 0 and not processing:
#         processing = True  # 인식 잠금
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             label = classes[class_ids[i]]
#             confidence = confidences[i]

#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0 or roi.shape[0] < 5 or roi.shape[1] < 5:
#                 continue

#             hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             avg_h = hsv_roi[:, :, 0].mean()
#             avg_s = hsv_roi[:, :, 1].mean()
#             avg_v = hsv_roi[:, :, 2].mean()
#             color = get_color_from_hsv(avg_h, avg_s, avg_v)

#             # 인식 시간 기록
#             recognized_time = datetime.datetime.now()
#             print(f"[인식] {label} ({color}) | 시간: {recognized_time.strftime('%Y-%m-%d %H:%M:%S')}")

#             # 🔽 아두이노 로봇팔 동작 부분 (예: 색상 따라 이동 위치 설정)
#             # import serial
#             # ser = serial.Serial('COM5', 9600, timeout=1)
#             # if color == "red":
#             #     ser.write(b"POSITION_1\n")
#             # elif color == "blue":
#             #     ser.write(b"POSITION_2\n")
#             # ...
#             # ser.close()

#             # 예시용 동작 대기 시간
#             time.sleep(3)  # 로봇팔이 물체를 이동 + 놓는 시간

#             placed_time = datetime.datetime.now()
#             print(f"[완료] {label} 놓음 | 시간: {placed_time.strftime('%Y-%m-%d %H:%M:%S')}")

#             # DB 저장
#             sql = "INSERT INTO object_log (label, color, recognized_time, placed_time) VALUES (%s, %s, %s, %s)"
#             cursor.execute(sql, (label, color, recognized_time, placed_time))
#             conn.commit()

#             break  # 하나만 처리하고 빠져나옴

#         processing = False  # 다시 인식 가능하게 설정

#     # 프레임 출력
#     cv2.imshow("YOLO + 로봇팔 플로우", frame)

#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# cursor.close()
# conn.close()
