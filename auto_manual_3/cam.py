# import cv2
# import numpy as np
# import time
# import serial
# import threading

# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# # 상태 변수
# mode = "idle"
# emergency_triggered = False
# remaining_cmds = []
# executed_log = []
# act_thread = None
# processing = False

# # 기능 함수
# def get_color_from_hsv(h, s, v):
#     if v < 40: return "black"
#     elif s < 30 and v > 200: return "white"
#     elif s < 40: return "gray"
#     elif h < 10 or h >= 160: return "red"
#     elif 35 <= h < 85: return "green"
#     elif 85 <= h < 110: return "blue"
#     else: return "other"

# def get_total_rotation():
#     return sum(val for act, val in executed_log if act == 'a')

# def get_total_distance():
#     return sum(abs(val) for act, val in executed_log if act == 'd')

# def send_and_log(command):
#     global executed_log
#     ser.write((command + "\n").encode())
#     print(f"[전송] {command}")
#     parts = command.strip().split(',')
#     if len(parts) == 3:
#         executed_log.append((parts[1], float(parts[2])))

# def reverse_log():
#     reversed_cmds = []
#     for act, val in reversed(executed_log):
#         if act in ['a', 'd']:
#             motor = '1' if act == 'a' else '2'
#             reversed_cmds.append(f"{motor},{act},{-val}")
#     return reversed_cmds

# def act_by_color(color):
#     global emergency_triggered, remaining_cmds, executed_log
#     if emergency_triggered:
#         return

#     executed_log.clear()

#     if color == "red":
#         print("[감지] 빨간 병 → 15cm 상승 + 180도 회전")
#         remaining_cmds = ["2,d,15", "1,a,180", "1,a,-180", "2,d,-15"]
#     elif color == "blue":
#         print("[감지] 파란 병 → 10cm 상승 + 30도 회전")
#         remaining_cmds = ["2,d,10", "1,a,30", "1,a,-30", "2,d,-10"]
#     else:
#         print(f"[무시] {color} 병")
#         return

#     for cmd in remaining_cmds[:]:
#         for _ in range(20):
#             if emergency_triggered:
#                 print("🚨 작업 중단됨")
#                 remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                 return
#             time.sleep(0.1)
#         send_and_log(cmd)

#     remaining_cmds = []
#     print("[완료] 병 작업 종료")

# def console_listener():
#     global mode, emergency_triggered, remaining_cmds, act_thread
#     while True:
#         cmd = input("\n입력 (a:자동 / m:수동 / q:정지 / e:비상 / r:재개 / reset:초기화): ").strip()
#         if cmd == 'a':
#             mode = "auto"
#             emergency_triggered = False
#             ser.write(b"a\n")
#             print("[모드] 자동 모드")
#         elif cmd == 'm':
#             mode = "manual"
#             emergency_triggered = False
#             ser.write(b"m\n")
#             print("[모드] 수동 모드")
#         elif cmd == 'q':
#             if mode == "manual":
#                 ser.write(b"q\n")
#                 print("🛑 수동 모터 정지")
#             else:
#                 print("[알림] q는 수동 모드에서만 작동")
#         elif cmd == 'e':
#             if mode == "auto":
#                 emergency_triggered = True
#                 ser.write(b"q\n")
#                 print("🚨 비상정지 요청됨!")

#                 if act_thread and act_thread.is_alive():
#                     print("⌛ 현재 동작 중단 대기 중...")
#                     act_thread.join(timeout=0.1)

#                 print(f"🌀 회전 누적: {get_total_rotation()}도")
#                 print(f"📏 이동 누적: {get_total_distance()}cm")
#             else:
#                 print("[알림] e는 자동 모드에서만 사용")
#         elif cmd == 'r':
#             if not remaining_cmds:
#                 print("[재개 불가] 남은 명령 없음")
#                 continue
#             emergency_triggered = False
#             print("[재개] 남은 명령 실행 중...")
#             for cmd in remaining_cmds[:]:
#                 for _ in range(20):
#                     if emergency_triggered:
#                         print("🚨 재개 도중 중단")
#                         remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                         return
#                     time.sleep(0.1)
#                 send_and_log(cmd)
#             remaining_cmds.clear()
#             print("[완료] 재개 완료")
#         elif cmd == 'reset':
#             rev_cmds = reverse_log()
#             print(f"[초기화] 원위치 복귀 시작 (거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도)")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[초기화 완료]")
#         else:
#             if mode == "manual" and ',' in cmd:
#                 ser.write((cmd + "\n").encode())
#                 print(f"[수동 전송] {cmd}")
#             else:
#                 print("[잘못된 입력 또는 모드 오류]")

# # 콘솔 입력 스레드 실행
# threading.Thread(target=console_listener, daemon=True).start()

# # YOLO 감지 루프
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("웹캠 실패")
#     exit()

# last_detection_time = 0
# cooldown = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if mode != "auto":
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     now = time.time()
#     if now - last_detection_time < cooldown:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes, confidences = [], []
#     for out in outs:
#         for det in out:
#             scores = det[5:]
#             class_id = np.argmax(scores)
#             conf = scores[class_id]
#             if conf > 0.3 and classes[class_id] == "bottle":
#                 x = int(det[0] * width - det[2] * width / 2)
#                 y = int(det[1] * height - det[3] * height / 2)
#                 w = int(det[2] * width)
#                 h = int(det[3] * height)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(conf))

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing and not emergency_triggered:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0:
#                 continue
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             h_avg = hsv[:, :, 0].mean()
#             s_avg = hsv[:, :, 1].mean()
#             v_avg = hsv[:, :, 2].mean()
#             color = get_color_from_hsv(h_avg, s_avg, v_avg)

#             # 👉 쓰레드로 act_by_color 실행
#             act_thread = threading.Thread(target=act_by_color, args=(color,))
#             act_thread.start()

#             last_detection_time = time.time()
#             break
#         processing = False

#     cv2.imshow("YOLO", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()






# import cv2
# import numpy as np
# import time
# import serial
# import threading

# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# # 상태 변수
# mode = "idle"
# emergency_triggered = False
# remaining_cmds = []
# executed_log = []
# act_thread = None
# processing = False

# # 기능 함수
# def get_color_from_hsv(h, s, v):
#     if v < 40: return "black"
#     elif s < 30 and v > 200: return "white"
#     elif s < 40: return "gray"
#     elif h < 10 or h >= 160: return "red"
#     elif 35 <= h < 85: return "green"
#     elif 85 <= h < 110: return "blue"
#     else: return "other"

# def get_total_rotation():
#     return sum(val for act, val in executed_log if act == 'a')

# def get_total_distance():
#     return sum(abs(val) for act, val in executed_log if act == 'd')

# def send_and_log(command):
#     global executed_log
#     ser.write((command + "\n").encode())
#     print(f"[전송] {command}")
#     parts = command.strip().split(',')
#     if len(parts) == 3:
#         executed_log.append((parts[1], float(parts[2])))

# def reverse_log():
#     reversed_cmds = []
#     for act, val in reversed(executed_log):
#         if act in ['a', 'd']:
#             motor = '1' if act == 'a' else '2'
#             reversed_cmds.append(f"{motor},{act},{-val}")
#     return reversed_cmds

# def act_by_color(color):
#     global emergency_triggered, remaining_cmds, executed_log
#     if emergency_triggered:
#         return

#     executed_log.clear()

#     if color == "red":
#         print("[감지] 빨간 병 → 15cm 상승 + 180도 회전")
#         remaining_cmds = ["2,d,15", "1,a,180", "1,a,-180", "2,d,-15"]
#     elif color == "blue":
#         print("[감지] 파란 병 → 10cm 상승 + 30도 회전")
#         remaining_cmds = ["2,d,10", "1,a,30", "1,a,-30", "2,d,-10"]
#     else:
#         print(f"[무시] {color} 병")
#         return

#     for cmd in remaining_cmds[:]:
#         for _ in range(20):
#             if emergency_triggered:
#                 print("🚨 작업 중단됨")
#                 remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                 return
#             time.sleep(0.1)
#         send_and_log(cmd)

#     remaining_cmds = []
#     print("[완료] 병 작업 종료")

# def console_listener():
#     global mode, emergency_triggered, remaining_cmds, act_thread

#     while True:
#         cmd = input("\n입력 (a:자동 / m:수동 / q:정지 / e:비상 / r:재개 / o:복귀 / reset:초기화): ").strip()
#         if cmd == 'a':
#             mode = "auto"
#             emergency_triggered = False
#             ser.write(b"a\n")
#             print("[모드] 자동 모드")

#         elif cmd == 'm':
#             mode = "manual"
#             emergency_triggered = False
#             ser.write(b"m\n")
#             print("[모드] 수동 모드")

#         elif cmd == 'q':
#             ser.write(b"q\n")
#             print("🛑 전체 모터 정지 요청됨")
#             emergency_triggered = True
#             if act_thread and act_thread.is_alive():
#                 print("⌛ 동작 종료 대기 중...")
#                 act_thread.join(timeout=0.1)
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")

#         elif cmd == 'o':
#             if not executed_log:
#                 print("[복귀 실패] 기록된 동작 없음")
#                 continue
#             rev_cmds = reverse_log()
#             print(f"[복귀 시작] 거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[복귀 완료]")

#         elif cmd == 'r':
#             if not remaining_cmds:
#                 print("[재개 불가] 남은 명령 없음")
#                 continue
#             emergency_triggered = False
#             print("[재개] 남은 명령 실행 중...")
#             for cmd in remaining_cmds[:]:
#                 for _ in range(20):
#                     if emergency_triggered:
#                         print("🚨 재개 도중 중단")
#                         remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                         return
#                     time.sleep(0.1)
#                 send_and_log(cmd)
#             remaining_cmds.clear()
#             print("[완료] 재개 완료")

#         elif cmd == 'reset':
#             rev_cmds = reverse_log()
#             print(f"[초기화] 원위치 복귀 시작 (거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도)")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[초기화 완료]")

#         else:
#             if mode == "manual" and ',' in cmd:
#                 ser.write((cmd + "\n").encode())
#                 print(f"[수동 전송] {cmd}")
#             else:
#                 print("[잘못된 입력 또는 모드 오류]")

# # 콘솔 입력 스레드 실행
# threading.Thread(target=console_listener, daemon=True).start()

# # YOLO 감지 루프
# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     print("웹캠 실패")
#     exit()

# last_detection_time = 0
# cooldown = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if mode != "auto":
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     now = time.time()
#     if now - last_detection_time < cooldown:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes, confidences = [], []
#     for out in outs:
#         for det in out:
#             scores = det[5:]
#             class_id = np.argmax(scores)
#             conf = scores[class_id]
#             if conf > 0.3 and classes[class_id] == "bottle":
#                 x = int(det[0] * width - det[2] * width / 2)
#                 y = int(det[1] * height - det[3] * height / 2)
#                 w = int(det[2] * width)
#                 h = int(det[3] * height)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(conf))

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing and not emergency_triggered:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0:
#                 continue
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             h_avg = hsv[:, :, 0].mean()
#             s_avg = hsv[:, :, 1].mean()
#             v_avg = hsv[:, :, 2].mean()
#             color = get_color_from_hsv(h_avg, s_avg, v_avg)

#             act_thread = threading.Thread(target=act_by_color, args=(color,))
#             act_thread.start()

#             last_detection_time = time.time()
#             break
#         processing = False

#     cv2.imshow("YOLO", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()







# import cv2
# import numpy as np
# import time
# import serial
# import threading

# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# mode = "idle"
# emergency_triggered = False
# remaining_cmds = []
# executed_log = []
# act_thread = None
# processing = False

# def get_color_from_hsv(h, s, v):
#     if v < 40: return "black"
#     elif s < 30 and v > 200: return "white"
#     elif s < 40: return "gray"
#     elif h < 10 or h >= 160: return "red"
#     elif 35 <= h < 85: return "green"
#     elif 85 <= h < 110: return "blue"
#     else: return "other"

# def get_total_rotation():
#     return sum(val for act, val in executed_log if act == 'a')

# def get_total_distance():
#     return sum(abs(val) for act, val in executed_log if act == 'd')

# def send_and_log(command):
#     global executed_log
#     ser.write((command + "\n").encode())
#     print(f"[전송] {command}")
#     parts = command.strip().split(',')
#     if len(parts) == 3:
#         executed_log.append((parts[1], float(parts[2])))

# def reverse_log():
#     reversed_cmds = []
#     for act, val in reversed(executed_log):
#         if act in ['a', 'd']:
#             motor = '1' if act == 'a' else '2'
#             reversed_cmds.append(f"{motor},{act},{-val}")
#     return reversed_cmds

# def act_by_color(color):
#     global emergency_triggered, remaining_cmds, executed_log, processing
#     if emergency_triggered:
#         processing = False
#         return

#     executed_log.clear()

#     if color == "red":
#         print("[감지] 빨간 병 → 15cm 상승 + 180도 회전")
#         remaining_cmds = ["2,d,15", "1,a,180", "1,a,-180", "2,d,-15"]
#     elif color == "blue":
#         print("[감지] 파란 병 → 10cm 상승 + 30도 회전")
#         remaining_cmds = ["2,d,10", "1,a,30", "1,a,-30", "2,d,-10"]
#     else:
#         print(f"[무시] {color} 병")
#         processing = False
#         return

#     for cmd in remaining_cmds[:]:
#         for _ in range(20):
#             if emergency_triggered:
#                 print("🚨 작업 중단됨")
#                 remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                 processing = False
#                 return
#             time.sleep(0.1)
#         send_and_log(cmd)

#     remaining_cmds = []
#     print("[완료] 병 작업 종료")
#     print(f"🌀 회전 누적: {get_total_rotation()}도")
#     print(f"📏 이동 누적: {get_total_distance()}cm")
#     processing = False

# def console_listener():
#     global mode, emergency_triggered, remaining_cmds, act_thread, processing

#     while True:
#         cmd = input("\n입력 (a:자동 / m:수동 / q:정지 / e:비상 / r:재개 / o:복귀 / reset:초기화): ").strip()
#         if cmd == 'a':
#             mode = "auto"
#             emergency_triggered = False
#             ser.write(b"a\n")
#             print("[모드] 자동 모드")

#         elif cmd == 'm':
#             mode = "manual"
#             emergency_triggered = False
#             ser.write(b"m\n")
#             print("[모드] 수동 모드")

#         elif cmd == 'q':
#             emergency_triggered = True
#             print("🛑 전체 모터 정지 요청됨")
#             ser.write(b"q\n")
#             if act_thread and act_thread.is_alive():
#                 print("⌛ 동작 종료 대기 중...")
#                 act_thread.join(timeout=0.1)
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             processing = False

#         elif cmd == 'o':
#             if not executed_log:
#                 print("[복귀 실패] 기록된 동작 없음")
#                 continue
#             rev_cmds = reverse_log()
#             print(f"[복귀 시작] 거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[복귀 완료]")

#         elif cmd == 'r':
#             if not remaining_cmds:
#                 print("[재개 불가] 남은 명령 없음")
#                 continue
#             emergency_triggered = False
#             print("[재개] 남은 명령 실행 중...")
#             for cmd in remaining_cmds[:]:
#                 for _ in range(20):
#                     if emergency_triggered:
#                         print("🚨 재개 도중 중단")
#                         remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                         return
#                     time.sleep(0.1)
#                 send_and_log(cmd)
#             remaining_cmds.clear()
#             print("[완료] 재개 완료")

#         elif cmd == 'reset':
#             rev_cmds = reverse_log()
#             print(f"[초기화] 원위치 복귀 시작 (거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도)")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[초기화 완료]")

#         else:
#             if mode == "manual" and ',' in cmd:
#                 ser.write((cmd + "\n").encode())
#                 print(f"[수동 전송] {cmd}")
#             else:
#                 print("[잘못된 입력 또는 모드 오류]")

# threading.Thread(target=console_listener, daemon=True).start()

# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     print("웹캠 실패")
#     exit()

# last_detection_time = 0
# cooldown = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if mode != "auto" or emergency_triggered:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     now = time.time()
#     if now - last_detection_time < cooldown:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes, confidences = [], []
#     for out in outs:
#         for det in out:
#             scores = det[5:]
#             class_id = np.argmax(scores)
#             conf = scores[class_id]
#             if conf > 0.3 and classes[class_id] == "bottle":
#                 x = int(det[0] * width - det[2] * width / 2)
#                 y = int(det[1] * height - det[3] * height / 2)
#                 w = int(det[2] * width)
#                 h = int(det[3] * height)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(conf))

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing and not emergency_triggered:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0:
#                 continue
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             h_avg = hsv[:, :, 0].mean()
#             s_avg = hsv[:, :, 1].mean()
#             v_avg = hsv[:, :, 2].mean()
#             color = get_color_from_hsv(h_avg, s_avg, v_avg)

#             act_thread = threading.Thread(target=act_by_color, args=(color,))
#             act_thread.start()
#             last_detection_time = time.time()
#             break

#     cv2.imshow("YOLO", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()










# # 제발 돼라
# import cv2
# import numpy as np
# import time
# import serial
# import threading

# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# mode = "idle"
# emergency_triggered = False
# remaining_cmds = []
# executed_log = []
# act_thread = None
# processing = False

# def get_color_from_hsv(h, s, v):
#     if v < 40: return "black"
#     elif s < 30 and v > 200: return "white"
#     elif s < 40: return "gray"
#     elif h < 10 or h >= 160: return "red"
#     elif 35 <= h < 85: return "green"
#     elif 85 <= h < 110: return "blue"
#     else: return "other"

# def get_total_rotation():
#     return sum(val for act, val in executed_log if act == 'a')

# def get_total_distance():
#     return sum(abs(val) for act, val in executed_log if act == 'd')

# def send_and_log(command):
#     global executed_log
#     ser.write((command + "\n").encode())
#     print(f"[전송] {command}")
#     parts = command.strip().split(',')
#     if len(parts) == 3:
#         executed_log.append((parts[1], float(parts[2])))

# def reverse_log():
#     reversed_cmds = []
#     for act, val in reversed(executed_log):
#         motor = '3' if act == 'a' else '2'  # 회전이면 3번 모터
#         reversed_cmds.append(f"{motor},{act},{-val}")
#     return reversed_cmds


# def act_by_color(color):
#     global emergency_triggered, remaining_cmds, executed_log, processing

#     if emergency_triggered:
#         processing = False
#         return

#     executed_log.clear()

#     if color == "red":
#         print("[감지] 빨간 병 → 15cm 상승 + 180도 회전")
#         remaining_cmds = ["2,d,15", "3,a,180", "3,a,-180", "2,d,-15"]
#     elif color == "blue":
#         print("[감지] 파란 병 → 10cm 상승 + 30도 회전")
#         remaining_cmds = ["2,d,5", "3,a,180", "3,a,-180", "2,d,-5"]
#     else:
#         print(f"[무시] {color} 병")
#         processing = False
#         return

#     for cmd in remaining_cmds[:]:
#         if emergency_triggered:
#             print("🚨 작업 중단됨 (시작 전)")
#             remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#             processing = False
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             return

#         for _ in range(20):
#             if emergency_triggered:
#                 print("🚨 작업 중단됨 (진행 중)")
#                 remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                 processing = False
#                 print(f"🌀 회전 누적: {get_total_rotation()}도")
#                 print(f"📏 이동 누적: {get_total_distance()}cm")
#                 return
#             time.sleep(0.1)

#         send_and_log(cmd)

#     remaining_cmds = []
#     print("[완료] 병 작업 종료")
#     print(f"🌀 회전 누적: {get_total_rotation()}도")
#     print(f"📏 이동 누적: {get_total_distance()}cm")
#     processing = False

# def console_listener():
#     global mode, emergency_triggered, remaining_cmds, act_thread, processing

#     while True:
#         cmd = input("\n입력 (a:자동 / m:수동 / q:정지 / e:비상 / r:재개 / o:복귀 / reset:초기화): ").strip()
#         if cmd == 'a':
#             mode = "auto"
#             emergency_triggered = False
#             ser.write(b"a\n")
#             print("[모드] 자동 모드")

#         elif cmd == 'm':
#             mode = "manual"
#             emergency_triggered = False
#             ser.write(b"m\n")
#             print("[모드] 수동 모드")

#         elif cmd == 'q':
#             emergency_triggered = True
#             print("🛑 전체 모터 정지 요청됨")
#             ser.write(b"q\n")
#             if act_thread and act_thread.is_alive():
#                 print("⌛ 동작 종료 대기 중...")
#                 act_thread.join(timeout=0.1)
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             processing = False

#         elif cmd == 'o':
#             if not executed_log:
#                 print("[복귀 실패] 기록된 동작 없음")
#                 continue
#             rev_cmds = reverse_log()
#             print(f"[복귀 시작] 거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[복귀 완료]")

#         elif cmd == 'r':
#             if not remaining_cmds:
#                 print("[재개 불가] 남은 명령 없음")
#                 continue
#             emergency_triggered = False
#             print("[재개] 남은 명령 실행 중...")
#             for cmd in remaining_cmds[:]:
#                 for _ in range(20):
#                     if emergency_triggered:
#                         print("🚨 재개 도중 중단")
#                         remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                         return
#                     time.sleep(0.1)
#                 send_and_log(cmd)
#             remaining_cmds.clear()
#             print("[완료] 재개 완료")

#         elif cmd == 'reset':
#             rev_cmds = reverse_log()
#             print(f"[초기화] 원위치 복귀 시작 (거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도)")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 time.sleep(2)
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[초기화 완료]")

#         else:
#             if mode == "manual" and ',' in cmd:
#                 ser.write((cmd + "\n").encode())
#                 print(f"[수동 전송] {cmd}")
#             else:
#                 print("[잘못된 입력 또는 모드 오류]")

# threading.Thread(target=console_listener, daemon=True).start()

# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     print("웹캠 실패")
#     exit()

# last_detection_time = 0
# cooldown = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if mode != "auto" or emergency_triggered:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     now = time.time()
#     if now - last_detection_time < cooldown:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes, confidences = [], []
#     for out in outs:
#         for det in out:
#             scores = det[5:]
#             class_id = np.argmax(scores)
#             conf = scores[class_id]
#             if conf > 0.3 and classes[class_id] == "bottle":
#                 x = int(det[0] * width - det[2] * width / 2)
#                 y = int(det[1] * height - det[3] * height / 2)
#                 w = int(det[2] * width)
#                 h = int(det[3] * height)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(conf))

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing and not emergency_triggered:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0:
#                 continue
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             h_avg = hsv[:, :, 0].mean()
#             s_avg = hsv[:, :, 1].mean()
#             v_avg = hsv[:, :, 2].mean()
#             color = get_color_from_hsv(h_avg, s_avg, v_avg)

#             act_thread = threading.Thread(target=act_by_color, args=(color,))
#             act_thread.start()
#             last_detection_time = time.time()
#             break

#     cv2.imshow("YOLO", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()


# import cv2
# import numpy as np
# import time
# import serial
# import threading

# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# mode = "idle"
# emergency_triggered = False
# remaining_cmds = []
# executed_log = []
# act_thread = None
# processing = False

# def get_color_from_hsv(h, s, v):
#     if v < 40: return "black"
#     elif s < 30 and v > 200: return "white"
#     elif s < 40: return "gray"
#     elif h < 10 or h >= 160: return "red"
#     elif 35 <= h < 85: return "green"
#     elif 85 <= h < 110: return "blue"
#     else: return "other"

# def get_total_rotation():
#     return sum(val for act, val in executed_log if act == 'a')

# def get_total_distance():
#     return sum(abs(val) for act, val in executed_log if act == 'd')

# def send_and_log(command):
#     global executed_log
#     ser.write((command + "\n").encode())
#     print(f"[전송] {command}")
#     time.sleep(0.1)  # 명령 전송 후 잠시 대기
    
#     parts = command.strip().split(',')
#     if len(parts) == 3:
#         executed_log.append((parts[1], float(parts[2])))

# def wait_for_arduino_response(timeout=10):
#     """아두이노로부터 응답 대기"""
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         if ser.in_waiting > 0:
#             response = ser.readline().decode('utf-8').strip()
#             if response.startswith("done"):
#                 print(f"[응답] {response}")
#                 return True
#             elif "[중단]" in response:
#                 print(f"[중단 응답] {response}")
#                 return False
#             print(f"[아두이노] {response}")
#         time.sleep(0.1)
#     print("[경고] 아두이노 응답 타임아웃")
#     return False

# def reverse_log():
#     reversed_cmds = []
#     for act, val in reversed(executed_log):
#         motor = '3' if act == 'a' else '2'  # 회전이면 3번 모터
#         reversed_cmds.append(f"{motor},{act},{-val}")
#     return reversed_cmds

# def act_by_color(color):
#     global emergency_triggered, remaining_cmds, executed_log, processing

#     if emergency_triggered:
#         processing = False
#         return

#     executed_log.clear()

#     if color == "red":
#         print("[감지] 빨간 병 → 15cm 상승 + 180도 회전")
#         remaining_cmds = ["2,d,15", "3,a,180", "3,a,-180", "2,d,-15"]
#     elif color == "blue":
#         print("[감지] 파란 병 → 10cm 상승 + 30도 회전")
#         remaining_cmds = ["2,d,5", "3,a,30", "3,a,-30", "2,d,-5"]
#     else:
#         print(f"[무시] {color} 병")
#         processing = False
#         return

#     for cmd in remaining_cmds[:]:
#         if emergency_triggered:
#             print("🚨 작업 중단됨 (시작 전)")
#             remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#             processing = False
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             return

#         print(f"[실행] {cmd} 명령어 실행 중...")
#         send_and_log(cmd)
        
#         # 명령 완료 대기
#         response_ok = wait_for_arduino_response()
#         if not response_ok or emergency_triggered:
#             print("🚨 작업 중단됨 (진행 중)")
#             remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#             processing = False
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             return

#     remaining_cmds = []
#     print("[완료] 병 작업 종료")
#     print(f"🌀 회전 누적: {get_total_rotation()}도")
#     print(f"📏 이동 누적: {get_total_distance()}cm")
#     processing = False

# def console_listener():
#     global mode, emergency_triggered, remaining_cmds, act_thread, processing

#     while True:
#         cmd = input("\n입력 (a:자동 / m:수동 / q:정지 / e:비상 / r:재개 / o:복귀 / reset:초기화): ").strip()
#         if cmd == 'a':
#             mode = "auto"
#             emergency_triggered = False
#             ser.write(b"a\n")
#             print("[모드] 자동 모드")

#         elif cmd == 'm':
#             mode = "manual"
#             emergency_triggered = False
#             ser.write(b"m\n")
#             print("[모드] 수동 모드")

#         elif cmd == 'q':
#             emergency_triggered = True
#             print("🛑 전체 모터 정지 요청됨")
#             ser.write(b"q\n")
#             if act_thread and act_thread.is_alive():
#                 print("⌛ 동작 종료 대기 중...")
#                 act_thread.join(timeout=0.1)
#             print(f"🌀 회전 누적: {get_total_rotation()}도")
#             print(f"📏 이동 누적: {get_total_distance()}cm")
#             processing = False

#         elif cmd == 'o':
#             if not executed_log:
#                 print("[복귀 실패] 기록된 동작 없음")
#                 continue
#             rev_cmds = reverse_log()
#             print(f"[복귀 시작] 거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 wait_for_arduino_response()
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[복귀 완료]")

#         elif cmd == 'r':
#             if not remaining_cmds:
#                 print("[재개 불가] 남은 명령 없음")
#                 continue
#             emergency_triggered = False
#             print("[재개] 남은 명령 실행 중...")
#             for cmd in remaining_cmds[:]:
#                 send_and_log(cmd)
#                 if not wait_for_arduino_response() or emergency_triggered:
#                     print("🚨 재개 도중 중단")
#                     remaining_cmds = remaining_cmds[remaining_cmds.index(cmd):]
#                     return
#             remaining_cmds.clear()
#             print("[완료] 재개 완료")

#         elif cmd == 'reset':
#             rev_cmds = reverse_log()
#             print(f"[초기화] 원위치 복귀 시작 (거리: {get_total_distance()}cm / 각도: {get_total_rotation()}도)")
#             for cmd in rev_cmds:
#                 send_and_log(cmd)
#                 wait_for_arduino_response()
#             executed_log.clear()
#             remaining_cmds.clear()
#             print("[초기화 완료]")

#         else:
#             if mode == "manual" and ',' in cmd:
#                 ser.write((cmd + "\n").encode())
#                 print(f"[수동 전송] {cmd}")
#             else:
#                 print("[잘못된 입력 또는 모드 오류]")

# threading.Thread(target=console_listener, daemon=True).start()

# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     print("웹캠 실패")
#     exit()

# last_detection_time = 0
# cooldown = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if mode != "auto" or emergency_triggered:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     now = time.time()
#     if now - last_detection_time < cooldown:
#         cv2.imshow("YOLO", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     boxes, confidences = [], []
#     for out in outs:
#         for det in out:
#             scores = det[5:]
#             class_id = np.argmax(scores)
#             conf = scores[class_id]
#             if conf > 0.3 and classes[class_id] == "bottle":
#                 x = int(det[0] * width - det[2] * width / 2)
#                 y = int(det[1] * height - det[3] * height / 2)
#                 w = int(det[2] * width)
#                 h = int(det[3] * height)
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(conf))

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing and not emergency_triggered:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0:
#                 continue
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             h_avg = hsv[:, :, 0].mean()
#             s_avg = hsv[:, :, 1].mean()
#             v_avg = hsv[:, :, 2].mean()
#             color = get_color_from_hsv(h_avg, s_avg, v_avg)

#             act_thread = threading.Thread(target=act_by_color, args=(color,))
#             act_thread.start()
#             last_detection_time = time.time()
#             break

#     cv2.imshow("YOLO", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()


# # 용찬이형 코드 되는거!!
# import cv2
# import numpy as np
# import time
# import serial

# # 시리얼 포트 연결
# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# # 색상 분류 함수
# def get_color_from_hsv(h, s, v):
#     if v < 40:
#         return "black"
#     elif s < 30 and v > 200:
#         return "white"
#     elif s < 40:
#         return "gray"
#     elif h < 10 or h >= 160:
#         return "red"
#     elif 35 <= h < 85:
#         return "green"
#     elif 85 <= h < 110:
#         return "blue"
#     else:
#         return "other"

# # 병 색상에 따른 동작 정의
# def act_by_color(color):
#     if color == "red":
#         print("[자동] 빨간 병 인식: 집게 후진 → 스텝 +50 → 하강 → 집게 전진 → 상승 → 스텝 -50")
#         ser.write(b"1,d,-5\n")
#         time.sleep(1)
#         ser.write(b"3,a,50\n")
#         time.sleep(2)
#         ser.write(b"2,d,-10\n")
#         time.sleep(2)
#         ser.write(b"1,d,5\n")
#         time.sleep(1)
#         ser.write(b"2,d,10\n")
#         time.sleep(2)
#         ser.write(b"3,a,-50\n")
#         time.sleep(2)
#         print("[완료] 빨간 병 작업 종료")

#     elif color == "blue":
#         print("[자동] 파란 병 인식: 집게 후진 → 스텝 -50 → 하강 → 집게 전진 → 상승 → 스텝 +50")
#         ser.write(b"1,d,-5\n")
#         time.sleep(1)
#         ser.write(b"3,a,-50\n")
#         time.sleep(2)
#         ser.write(b"2,d,-10\n")
#         time.sleep(2)
#         ser.write(b"1,d,5\n")
#         time.sleep(1)
#         ser.write(b"2,d,10\n")
#         time.sleep(2)
#         ser.write(b"3,a,50\n")
#         time.sleep(2)
#         print("[완료] 파란 병 작업 종료")

#     else:
#         print(f"[무시] 인식된 병 색상: {color} → 동작 없음")

# # 카메라 실행
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("웹캠 열기 실패")
#     exit()

# processing = False
# cooldown_time = 3
# last_detection_time = 0

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     current_time = time.time()
#     if current_time - last_detection_time < cooldown_time:
#         cv2.imshow("YOLO Object Detection", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
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
#             if confidence > 0.3:
#                 label = classes[class_id]
#                 if label != "bottle":
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

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0 or roi.shape[0] < 5 or roi.shape[1] < 5:
#                 continue
#             hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             avg_h = hsv_roi[:, :, 0].mean()
#             avg_s = hsv_roi[:, :, 1].mean()
#             avg_v = hsv_roi[:, :, 2].mean()
#             color = get_color_from_hsv(avg_h, avg_s, avg_v)

#             act_by_color(color)
#             last_detection_time = time.time()
#             break
#         processing = False

#     cv2.imshow("YOLO Object Detection", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()




# #이전꺼(12:40분꺼)
# import cv2
# import numpy as np
# import time
# import serial
# import threading

# # 시리얼 포트 연결
# ser = serial.Serial('COM5', 9600, timeout=1)
# time.sleep(2)

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

# stop_flag = False
# mode = "manual"  # 초기 모드는 수동

# # HSV 색상 인식 함수
# def get_color_from_hsv(h, s, v):
#     if v < 40:
#         return "black"
#     elif s < 30 and v > 200:
#         return "white"
#     elif s < 40:
#         return "gray"
#     elif h < 10 or h >= 160:
#         return "red"
#     elif 35 <= h < 85:
#         return "green"
#     elif 85 <= h < 110:
#         return "blue"
#     else:
#         return "other"

# def act_by_color(color):
#     if color == "red":
#         print("[빨강] 집게 5cm → 스텝모터 50도 → -10cm → 집게 -5cm → 10cm")
#         ser.write(b"1,d,5\n")
#         time.sleep(2)
#         ser.write(b"3,a,50\n")
#         time.sleep(2)
#         ser.write(b"2,d,-10\n")
#         time.sleep(2)
#         ser.write(b"1,d,-5\n")
#         time.sleep(2)
#         ser.write(b"2,d,10\n")
#         time.sleep(2)
#         print("[빨강] 작업 종료")
#     else:
#         print(f"[무시] 병 감지됨 (색상: {color})")

# # 콘솔 입력 쓰레드
# def console_input_listener():
#     global stop_flag, mode
#     while True:
#         cmd = input("입력(m/a/q/명령): ").strip()
#         if cmd == 'q':
#             stop_flag = True
#             ser.write(b"q\n")
#         elif cmd == 'a':
#             mode = "auto"
#             print("[모드 전환] 자동 모드")
#         elif cmd == 'm':
#             mode = "manual"
#             print("[모드 전환] 수동 모드")
#         else:
#             stop_flag = False
#             ser.write((cmd + "\n").encode())

# threading.Thread(target=console_input_listener, daemon=True).start()

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("웹캠 열기 실패")
#     exit()

# processing = False
# last_detection_time = 0
# cooldown_duration = 3

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     current_time = time.time()
#     if mode != "auto":
#         cv2.imshow("YOLO: 병 감지", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     if current_time - last_detection_time < cooldown_duration:
#         cv2.imshow("YOLO: 병 감지", frame)
#         if cv2.waitKey(1) == 27:
#             break
#         continue

#     height, width = frame.shape[:2]
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
#             if confidence > 0.3:
#                 label = classes[class_id]
#                 if label != "bottle":
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

#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

#     if len(indexes) > 0 and not processing:
#         processing = True
#         for i in indexes:
#             i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
#             x, y, w, h = boxes[i]
#             roi = frame[y:y + h, x:x + w]
#             if roi.size == 0 or roi.shape[0] < 5 or roi.shape[1] < 5:
#                 continue
#             hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             avg_h = hsv_roi[:, :, 0].mean()
#             avg_s = hsv_roi[:, :, 1].mean()
#             avg_v = hsv_roi[:, :, 2].mean()
#             color = get_color_from_hsv(avg_h, avg_s, avg_v)
#             act_by_color(color)
#             last_detection_time = time.time()
#             break
#         processing = False

#     cv2.imshow("YOLO: 병 감지", frame)
#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()



#05.07, 11:39
import cv2
import numpy as np
import time
import serial

# 아두이노 시리얼 연결
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# YOLO 설정
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

processing = False
cap = cv2.VideoCapture(0)

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

def send_command(cmd):
    print(f"[전송] {cmd}")
    ser.write((cmd + "\n").encode())
    time.sleep(1.5)

# 자동 모드로 설정
ser.write(b"a\n")
time.sleep(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3 and classes[class_id] == "bottle":
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

    if len(indexes) > 0 and not processing:
        processing = True
        for i in indexes:
            i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
            x, y, w, h = boxes[i]
            roi = frame[y:y + h, x:x + w]
            if roi.size == 0:
                continue

            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            avg_h = hsv_roi[:, :, 0].mean()
            avg_s = hsv_roi[:, :, 1].mean()
            avg_v = hsv_roi[:, :, 2].mean()
            color = get_color_from_hsv(avg_h, avg_s, avg_v)

            if color == "red":
                print("[자동] 빨간 병 인식")
                send_command("1,d,-8")
                send_command("3,a,90")
                send_command("2,d,-7") 
                send_command("1,d,8")
                time.sleep(3)
                send_command("2,d,10")
                send_command("3,a,-90")
                send_command("2,d,-3")

            elif color == "blue":
                print("[자동] 파란 병 인식")
                send_command("1,d,-8")
                send_command("3,a,-90")
                send_command("2,d,-7")
                send_command("1,d,8")
                time.sleep(3)
                send_command("2,d,10")
                send_command("3,a,90")
                send_command("2,d,-3")

            elif color == "green":
                print("[자동] 초록 병 인식")
                send_command("1,d,-8")
                send_command("3,a,-180")
                send_command("2,d,-12")
                send_command("1,d,8")
                time.sleep(3)
                send_command("2,d,15")
                send_command("3,a,180")
                send_command("2,d,-3")

            else:
                print(f"[무시] 병 인식됨 (색상: {color})")

            break
        processing = False

    cv2.imshow("YOLO 병 색상 인식", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

