//// <공통 설정>
//#include <Arduino.h>
//
//// <STEP 모터 설정>
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//float yellowGearAngle = 0;
//bool stepMotorRunning = false;
//
//// <DC모터 설정>
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_PIN 2
//
//int motor_speed = 220;
//volatile long encoderCount = 0;
//
//// <1번 모터 설정>
//#define IN3 9
//#define IN4 10
//
//// <기어 및 보정 설정>
//const float motor_gear_diameter = 7.0;
//const float second_gear_diameter = 4.0;
//const float final_gear_diameter = 3.0;
//const float pi = 3.1415;
//const float distance_correction_factor = 2.765;
//
//// 상태 변수
//bool stopRequested = false;
//bool manualMode = false;
//bool autoMode = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//
//const int stepDelayMicros = 20;
//
//// 함수 선언
//void checkSerialInput();
//void rotateStepMotor(float yellowDegree);
//void moveDCMotorDistance(float distance_cm);
//float distanceToMotorAngle(float distance_cm);
//void motor_forward();
//void motor_backward();
//void motor_stop();
//void motor1_forward();
//void motor1_backward();
//void motor1_stop();
//void emergency_stop();
//void encoderISR();
//
//void setup() {
//  Serial.begin(9600);
//  pinMode(stepStepPin, OUTPUT);
//  pinMode(stepDirPin, OUTPUT);
//  pinMode(IN1, OUTPUT);
//  pinMode(IN2, OUTPUT);
//  pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT);
//  pinMode(IN4, OUTPUT);
//  pinMode(ENCODER_PIN, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_PIN), encoderISR, RISING);
//
//  Serial.println("[Arduino] 대기 중: 'a' 입력 시 자동 모드 활성화");
//}
//
//void loop() {
//  if (Serial.available()) {
//    checkSerialInput();
//  }
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(stepDelayMicros);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(stepDelayMicros);
//    }
//  }
//}
//
//void checkSerialInput() {
//  String input = Serial.readStringUntil('\n');
//  input.trim();
//
//  if (input.equalsIgnoreCase("q")) {
//    emergency_stop();
//  } else if (input.equalsIgnoreCase("m")) {
//    manualMode = true;
//    autoMode = false;
//    Serial.println("[모드] 수동 모드");
//  } else if (input.equalsIgnoreCase("a")) {
//    manualMode = false;
//    autoMode = true;
//    Serial.println("[모드] 자동 모드");
//  } else if (manualMode && input.indexOf(',') > 0) {
//    int commaIdx = input.indexOf(',');
//    int motor = input.substring(0, commaIdx).toInt();
//    int direction = input.substring(commaIdx + 1).toInt();
//    stopRequested = false;
//
//    if (motor == 1) {
//      direction == 1 ? motor1_forward() : motor1_backward();
//    } else if (motor == 2) {
//      direction == 1 ? motor_forward() : motor_backward();
//    } else if (motor == 3) {
//      stepManualForward = direction == 1;
//      stepManualBackward = direction == 2;
//    }
//  } else if (autoMode && input.indexOf(',') > 0) {
//    int firstComma = input.indexOf(',');
//    int secondComma = input.indexOf(',', firstComma + 1);
//    if (firstComma > 0 && secondComma > firstComma) {
//      String motorStr = input.substring(0, firstComma);
//      String modeStr = input.substring(firstComma + 1, secondComma);
//      String valueStr = input.substring(secondComma + 1);
//
//      int motorSelect = motorStr.toInt();
//      char mode = modeStr.charAt(0);
//      float value = valueStr.toFloat();
//
//      stopRequested = false;
//      if (motorSelect == 1 && mode == 'a') rotateStepMotor(value);
//      else if (motorSelect == 2 && mode == 'd') moveDCMotorDistance(value);
//    }
//  }
//}
//
//void rotateStepMotor(float yellowDegree) {
//  stopRequested = false;
//  stepMotorRunning = true;
//  bool clockwise = yellowDegree >= 0;
//  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);
//
//  float motorDegree = abs(yellowDegree) * 360.0;
//  long stepsToMove = round((motorDegree / 360.0) * stepsPerRevolution);
//
//  for (long i = 0; i < stepsToMove; i++) {
//    if (stopRequested) break;
//    digitalWrite(stepStepPin, HIGH);
//    delayMicroseconds(stepDelayMicros);
//    digitalWrite(stepStepPin, LOW);
//    delayMicroseconds(stepDelayMicros);
//  }
//
//  stepMotorRunning = false;
//}
//
//void moveDCMotorDistance(float distance_cm) {
//  encoderCount = 0;
//  float angle = distanceToMotorAngle(distance_cm);
//  distance_cm >= 0 ? motor_forward() : motor_backward();
//
//  unsigned long moveTime = (unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor);
//  delay(moveTime);
//  motor_stop();
//}
//
//float distanceToMotorAngle(float distance_cm) {
//  float gear_ratio = motor_gear_diameter / second_gear_diameter;
//  float final_circumference = pi * final_gear_diameter;
//  return (distance_cm * 360.0) / (gear_ratio * final_circumference);
//}
//
//void motor_forward() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor_backward() {
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor_stop() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//
//void motor1_forward() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, HIGH);
//}
//
//void motor1_backward() {
//  digitalWrite(IN3, HIGH);
//  digitalWrite(IN4, LOW);
//}
//
//void motor1_stop() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, LOW);
//}
//
//void emergency_stop() {
//  motor_stop();
//  motor1_stop();
//  stopRequested = true;
//  stepManualForward = false;
//  stepManualBackward = false;
//  stepMotorRunning = false;
//  Serial.println("[STOP] 긴급 정지 완료");
//}
//
//void encoderISR() {
//  encoderCount++;
//}






//// 제발되라
//
//#include <Arduino.h>
//
//// 모터 핀 설정
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 20;
//
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2  // 상하 DC 모터 엔코더
//
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4  // 집게 모터 엔코더
//
//// 기어 및 변환 설정
//const float pulsesPerRevolution = 660.0; // 집게 회전 모터 기준
//const float cm_per_pulse = 0.0025;       // 상하 모터 기준 (보정됨)
//const float deg_per_pulse = 360.0 / pulsesPerRevolution;
//
//volatile long encoderCount1 = 0;
//volatile long encoderCount2 = 0;
//
//bool manualMode = false;
//bool stopRequested = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//bool clawForward = false;
//bool clawBackward = false;
//int motor_speed = 200;
//
//void setup() {
//  Serial.begin(9600);
//
//  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
//  pinMode(stepDirPin, OUTPUT); pinMode(stepStepPin, OUTPUT);
//
//  pinMode(ENCODER_1, INPUT_PULLUP);
//  pinMode(ENCODER_2, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_1), encoderISR1, RISING);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_2), encoderISR2, RISING);
//
//  Serial.println("[Arduino] 대기 중");
//}
//
//void loop() {
//  if (Serial.available()) checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    }
//
//    if (clawForward) {
//      digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
//      analogWrite(ENB, motor_speed);
//    } else if (clawBackward) {
//      digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
//      analogWrite(ENB, motor_speed);
//    }
//  }
//}
//
//void checkSerialInput() {
//  String input = Serial.readStringUntil('\n');
//  input.trim();
//
//  if (input == "q") {
//    stopAll();
//  } else if (input == "m") {
//    manualMode = true;
//    stopRequested = false;
//    Serial.println("[모드] 수동");
//  } else if (input == "a") {
//    manualMode = false;
//    stopRequested = false;
//    Serial.println("[모드] 자동");
//  } else if (input.indexOf(',') > 0) {
//    int first = input.indexOf(',');
//    int second = input.indexOf(',', first + 1);
//
//    if (second > 0) {
//      int motor = input.substring(0, first).toInt();
//      char mode = input.charAt(first + 1);
//      float val = input.substring(second + 1).toFloat();
//
//      stopRequested = false;
//      if (motor == 2 && mode == 'd') moveDC(val);
//      else if (motor == 3 && mode == 'a') rotateStepper(val);
//    } else {
//      int motor = input.substring(0, first).toInt();
//      int dir = input.substring(first + 1).toInt();
//
//      stopRequested = false;
//      if (motor == 1) {
//        clawForward = (dir == 2);
//        clawBackward = (dir == 1);
//      } else if (motor == 2) {
//        dir == 1 ? motorDown() : motorUp();
//      } else if (motor == 3) {
//        stepManualForward = (dir == 1);
//        stepManualBackward = (dir == 2);
//      }
//    }
//  }
//}
//
//void rotateStepper(float deg) {
//  long steps = abs(deg) * stepsPerRevolution / 360.0;
//  digitalWrite(stepDirPin, deg >= 0 ? HIGH : LOW);
//
//  for (long i = 0; i < steps; i++) {
//    if (stopRequested) break;
//    digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//    digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//  }
//
//  Serial.print("done,3,a,"); Serial.println(deg, 2);
//}
//
//void moveDC(float cm) {
//  encoderCount2 = 0;
//  stopRequested = false;
//
//  if (cm >= 0) motorUp();
//  else motorDown();
//
//  delay((unsigned long)(abs(cm) * 100));
//  motorStop();
//  Serial.print("done,2,d,"); Serial.println(cm, 2);
//}
//
//void motorUp() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//void motorDown() {
//  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//void motorStop() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//void clawStop() {
//  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void stopAll() {
//  stopRequested = true;
//  stepManualForward = false;
//  stepManualBackward = false;
//  clawForward = false;
//  clawBackward = false;
//  motorStop(); clawStop();
//
//  Serial.println("[STOP] 전체 정지됨");
//  Serial.print("집게 회전각(°): "); Serial.println(encoderCount1 * deg_per_pulse, 2);
//  Serial.print("상하 이동 거리(cm): "); Serial.println(encoderCount2 * cm_per_pulse, 2);
//}
//
//void encoderISR1() { encoderCount1++; }
//void encoderISR2() { encoderCount2++; }



// 05.03.11:27
//#include <Arduino.h>
//
//// 모터 핀 설정
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 20;
//
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2  // 상하 DC 모터 엔코더
//
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4  // 집게 모터 엔코더
//
//// 기어 및 변환 설정
//const float pulsesPerRevolution = 660.0; // 집게 회전 모터 기준
//const float cm_per_pulse = 0.0025;       // 상하 모터 기준 (보정됨)
//const float deg_per_pulse = 360.0 / pulsesPerRevolution;
//
//volatile long encoderCount1 = 0;
//volatile long encoderCount2 = 0;
//
//bool manualMode = false;
//bool stopRequested = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//bool clawForward = false;
//bool clawBackward = false;
//int motor_speed = 200;
//
//// 명령 처리 중 상태
//bool processingCommand = false;
//
//void setup() {
//  Serial.begin(9600);
//
//  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
//  pinMode(stepDirPin, OUTPUT); pinMode(stepStepPin, OUTPUT);
//
//  pinMode(ENCODER_1, INPUT_PULLUP);
//  pinMode(ENCODER_2, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_1), encoderISR1, RISING);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_2), encoderISR2, RISING);
//
//  // 초기화 시 모든 모터 정지
//  stopAll();
//  
//  Serial.println("[Arduino] 대기 중");
//}
//
//void loop() {
//  if (Serial.available()) checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    }
//
//    if (clawForward) {
//      digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
//      analogWrite(ENB, motor_speed);
//    } else if (clawBackward) {
//      digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
//      analogWrite(ENB, motor_speed);
//    }
//  }
//}
//
//void checkSerialInput() {
//  String input = Serial.readStringUntil('\n');
//  input.trim();
//
//  // 현재 명령 실행 중이면, q(중지) 외에는 무시
//  if (processingCommand && input != "q") {
//    Serial.println("[경고] 이전 명령 처리 중");
//    return;
//  }
//
//  if (input == "q") {
//    stopAll();
//  } else if (input == "m") {
//    manualMode = true;
//    stopRequested = false;
//    Serial.println("[모드] 수동");
//  } else if (input == "a") {
//    manualMode = false;
//    stopRequested = false;
//    Serial.println("[모드] 자동");
//  } else if (input.indexOf(',') > 0) {
//    int first = input.indexOf(',');
//    int second = input.indexOf(',', first + 1);
//
//    if (second > 0) {
//      int motor = input.substring(0, first).toInt();
//      char mode = input.charAt(first + 1);
//      float val = input.substring(second + 1).toFloat();
//
//      Serial.print("[명령 수신] 모터: "); 
//      Serial.print(motor); 
//      Serial.print(", 모드: "); 
//      Serial.print(mode); 
//      Serial.print(", 값: "); 
//      Serial.println(val);
//
//      stopRequested = false;
//      
//      if (motor == 2 && mode == 'd') {
//        processingCommand = true;
//        moveDC(val);
//        processingCommand = false;
//      }
//      else if (motor == 3 && mode == 'a') {
//        processingCommand = true;
//        Serial.print("[회전 시작] "); 
//        Serial.print(val); 
//        Serial.println("도");
//        rotateStepper(val);
//        Serial.println("[회전 완료]");
//        processingCommand = false;
//      }
//    } else {
//      int motor = input.substring(0, first).toInt();
//      int dir = input.substring(first + 1).toInt();
//
//      stopRequested = false;
//      if (motor == 1) {
//        clawForward = (dir == 2);
//        clawBackward = (dir == 1);
//      } else if (motor == 2) {
//        dir == 1 ? motorDown() : motorUp();
//      } else if (motor == 3) {
//        stepManualForward = (dir == 1);
//        stepManualBackward = (dir == 2);
//      }
//    }
//  }
//}
//
//void rotateStepper(float deg) {
//  long steps = abs(deg) * stepsPerRevolution / 360.0;
//  digitalWrite(stepDirPin, deg >= 0 ? HIGH : LOW);
//
//  Serial.print("[스텝 계산] ");
//  Serial.print(deg);
//  Serial.print("도 = ");
//  Serial.print(steps);
//  Serial.println("스텝");
//
//  // 1000스텝마다 상태 출력 (디버깅용)
//  long lastReport = 0;
//  
//  for (long i = 0; i < steps; i++) {
//    if (stopRequested) {
//      Serial.println("[중단] 회전 중지 요청");
//      break;
//    }
//    
//    // 상태 보고
//    if (i - lastReport >= 1000) {
//      Serial.print("[진행] ");
//      Serial.print(i);
//      Serial.print("/");
//      Serial.print(steps);
//      Serial.println(" 스텝");
//      lastReport = i;
//    }
//    
//    digitalWrite(stepStepPin, HIGH); 
//    delayMicroseconds(stepDelayMicros);
//    digitalWrite(stepStepPin, LOW);  
//    delayMicroseconds(stepDelayMicros);
//  }
//
//  Serial.print("done,3,a,"); 
//  Serial.println(deg, 2);
//}
//
//void moveDC(float cm) {
//  encoderCount2 = 0;
//  stopRequested = false;
//
//  if (cm >= 0) motorUp();
//  else motorDown();
//
//  // 이동 시간 계산 후 대기
//  unsigned long moveTime = (unsigned long)(abs(cm) * 100);
//  Serial.print("[이동] "); 
//  Serial.print(cm); 
//  Serial.print("cm ("); 
//  Serial.print(moveTime); 
//  Serial.println("ms)");
//  
//  delay(moveTime);
//  motorStop();
//  
//  Serial.print("done,2,d,"); 
//  Serial.println(cm, 2);
//}
//
//void motorUp() {
//  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//void motorDown() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//void motorStop() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//void clawStop() {
//  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void stopAll() {
//  stopRequested = true;
//  processingCommand = false; // 명령 처리 상태 초기화
//  stepManualForward = false;
//  stepManualBackward = false;
//  clawForward = false;
//  clawBackward = false;
//  motorStop(); clawStop();
//
//  Serial.println("[STOP] 전체 정지됨");
//  Serial.print("집게 회전각(°): "); Serial.println(encoderCount1 * deg_per_pulse, 2);
//  Serial.print("상하 이동 거리(cm): "); Serial.println(encoderCount2 * cm_per_pulse, 2);
//}
//
//void encoderISR1() { encoderCount1++; }
//void encoderISR2() { encoderCount2++; }



//#include <Arduino.h>
//
//// 모터 핀 설정
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 20;
//
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2  // 상하 DC 모터 엔코더
//
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4  // 집게 모터 엔코더
//
//// 기어 및 변환 설정
//const float pulsesPerRevolution = 660.0; // 집게 회전 모터 기준
//const float cm_per_pulse = 0.0025;       // 상하 모터 기준 (보정됨)
//const float deg_per_pulse = 360.0 / pulsesPerRevolution;
//
//volatile long encoderCount1 = 0;
//volatile long encoderCount2 = 0;
//
//bool manualMode = false;
//bool stopRequested = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//bool clawForward = false;
//bool clawBackward = false;
//int motor_speed = 200;
//
//// 명령 처리 중 상태
//volatile bool processingCommand = false;
//
//void setup() {
//  Serial.begin(9600);
//
//  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
//  pinMode(stepDirPin, OUTPUT); pinMode(stepStepPin, OUTPUT);
//
//  pinMode(ENCODER_1, INPUT_PULLUP);
//  pinMode(ENCODER_2, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_1), encoderISR1, RISING);
//  attachInterrupt(digitalPinToInterrupt(ENCODER_2), encoderISR2, RISING);
//
//  // 초기화 시 모든 모터 정지
//  stopAll();
//  
//  Serial.println("[Arduino] 대기 중");
//}
//
//void loop() {
//  if (Serial.available()) checkSerialInput();
//
//  // 수동 모드일 때 계속 스텝 명령 보내기
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH); delayMicroseconds(stepDelayMicros);
//      digitalWrite(stepStepPin, LOW);  delayMicroseconds(stepDelayMicros);
//    }
//
//    if (clawForward) {
//      digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
//      analogWrite(ENB, motor_speed);
//    } else if (clawBackward) {
//      digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
//      analogWrite(ENB, motor_speed);
//    }
//  }
//}
//
//void checkSerialInput() {
//  String input = Serial.readStringUntil('\n');
//  input.trim();
//
//  // q 명령어는 항상 처리
//  if (input == "q") {
//    stopAll();
//    return;
//  }
//
//  // 현재 명령 실행 중이면 대부분의 새 명령 무시 (q 제외)
//  if (processingCommand) {
//    Serial.println("[경고] 이전 명령 처리 중");
//    return;
//  }
//
//  if (input == "m") {
//    manualMode = true;
//    stopRequested = false;
//    Serial.println("[모드] 수동");
//  } else if (input == "a") {
//    manualMode = false;
//    stopRequested = false;
//    Serial.println("[모드] 자동");
//  } else if (input.indexOf(',') > 0) {
//    int first = input.indexOf(',');
//    int second = input.indexOf(',', first + 1);
//
//    if (second > 0) {
//      int motor = input.substring(0, first).toInt();
//      char mode = input.charAt(first + 1);
//      float val = input.substring(second + 1).toFloat();
//
//      Serial.print("[명령 수신] 모터: "); 
//      Serial.print(motor); 
//      Serial.print(", 모드: "); 
//      Serial.print(mode); 
//      Serial.print(", 값: "); 
//      Serial.println(val);
//
//      stopRequested = false;
//      
//      if (motor == 2 && mode == 'd') {
//        processingCommand = true;
//        moveDC(val);
//        processingCommand = false;
//      }
//      else if (motor == 3 && mode == 'a') {
//        processingCommand = true;
//        Serial.print("[회전 시작] "); 
//        Serial.print(val); 
//        Serial.println("도");
//        rotateStepper(val);
//        Serial.println("[회전 완료]");
//        processingCommand = false;
//      }
//    } else {
//      int motor = input.substring(0, first).toInt();
//      int dir = input.substring(first + 1).toInt();
//
//      stopRequested = false;
//      if (motor == 1) {
//        clawForward = (dir == 2);
//        clawBackward = (dir == 1);
//      } else if (motor == 2) {
//        dir == 1 ? motorDown() : motorUp();
//      } else if (motor == 3) {
//        stepManualForward = (dir == 1);
//        stepManualBackward = (dir == 2);
//      }
//    }
//  }
//}
//
//void rotateStepper(float deg) {
//  long steps = abs(deg) * stepsPerRevolution / 360.0;
//  digitalWrite(stepDirPin, deg >= 0 ? HIGH : LOW);
//
//  Serial.print("[스텝 계산] ");
//  Serial.print(deg);
//  Serial.print("도 = ");
//  Serial.print(steps);
//  Serial.println("스텝");
//
//  // 1000스텝마다 상태 출력 (디버깅용)
//  long lastReport = 0;
//  
//  for (long i = 0; i < steps; i++) {
//    if (stopRequested) {
//      Serial.println("[중단] 회전 중지 요청");
//      break;
//    }
//    
//    // 상태 보고
//    if (i - lastReport >= 1000) {
//      Serial.print("[진행] ");
//      Serial.print(i);
//      Serial.print("/");
//      Serial.print(steps);
//      Serial.println(" 스텝");
//      lastReport = i;
//    }
//    
//    digitalWrite(stepStepPin, HIGH); 
//    delayMicroseconds(stepDelayMicros);
//    digitalWrite(stepStepPin, LOW);  
//    delayMicroseconds(stepDelayMicros);
//  }
//
//  Serial.print("done,3,a,"); 
//  Serial.println(deg, 2);
//}
//
//void moveDC(float cm) {
//  encoderCount2 = 0;
//  stopRequested = false;
//
//  if (cm >= 0) motorUp();
//  else motorDown();
//
//  // 이동 시간 계산 후 대기
//  unsigned long moveTime = (unsigned long)(abs(cm) * 100);
//  Serial.print("[이동] "); 
//  Serial.print(cm); 
//  Serial.print("cm ("); 
//  Serial.print(moveTime); 
//  Serial.println("ms)");
//  
//  delay(moveTime);
//  motorStop();
//  
//  Serial.print("done,2,d,"); 
//  Serial.println(cm, 2);
//}
//
//void motorUp() {
//  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//void motorDown() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//void motorStop() {
//  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//void clawStop() {
//  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void stopAll() {
//  stopRequested = true;
//  processingCommand = false; // 명령 처리 상태 초기화
//  stepManualForward = false;
//  stepManualBackward = false;
//  clawForward = false;
//  clawBackward = false;
//  motorStop(); clawStop();
//
//  Serial.println("[STOP] 전체 정지됨");
//  Serial.print("집게 회전각(°): "); Serial.println(encoderCount1 * deg_per_pulse, 2);
//  Serial.print("상하 이동 거리(cm): "); Serial.println(encoderCount2 * cm_per_pulse, 2);
//}
//
//void encoderISR1() { encoderCount1++; }
//void encoderISR2() { encoderCount2++; }




//// 용찬이형 코드 되는거!
//// <공통 설정>
//#include <Arduino.h>
//
//// <3번 STEP 모터 설정>
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 20;
//float yellowGearAngle = 0;
//bool stepMotorRunning = false;
//
//// <2번 모터: 상하 DC 모터>
//#define ENA 6    
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2
//int motor_speed = 200;
//volatile long encoderCount = 0;
//
//// <1번 모터: 집게 DC 모터>
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4
//
//// <기어 및 이동 계산 설정>
//const float motor_gear_diameter = 7.0;
//const float second_gear_diameter = 4.0;
//const float final_gear_diameter = 3.0;
//const float pi = 3.1415;
//
//// <보정 비율 설정>
//const float distance_correction_factor = 2.7;
//
//bool stopRequested = false;
//bool autoMode = false;
//bool manualMode = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//
//void setup() {
//  Serial.begin(9600);
//  pinMode(stepStepPin, OUTPUT);
//  pinMode(stepDirPin, OUTPUT);
//  pinMode(IN1, OUTPUT);
//  pinMode(IN2, OUTPUT);
//  pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT);
//  pinMode(IN4, OUTPUT);
//  pinMode(ENB, OUTPUT);
//
//  Serial.println("입력 형식: 모드(a/m), 정지(q), 또는 모터번호,명령,값");
//  Serial.println("예시) a: 자동 모드 전환");
//  Serial.println("예시) m: 수동 모드 전환");
//  Serial.println("예시) 1,d,5 : 집게팔 모터 5cm 이동");
//  Serial.println("예시) 3,a,90 : 스텝모터 90도 회전");
//  Serial.println("예시) 2,d,10 : DC모터 10cm 이동");
//  Serial.println("예시) q : 긴급 정지");
//}
//
//void loop() {
//  checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(500);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(500);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(500);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(500);
//    }
//  }
//}
//
//void checkSerialInput() {
//  if (Serial.available() > 0) {
//    String input = Serial.readStringUntil('\n');
//    input.trim();
//
//    if (input.equalsIgnoreCase("q")) {
//      stopRequested = true;
//      emergency_stop();
//    } else if (input.equalsIgnoreCase("a")) {
//      autoMode = true;
//      manualMode = false;
//      Serial.println("자동 모드 시작");
//      executeAutoSequence();
//    } else if (input.equalsIgnoreCase("m")) {
//      autoMode = false;
//      manualMode = true;
//      Serial.println("수동 모드 시작");
//    } else if (manualMode && input.indexOf(',') > 0) {
//      int commaIdx = input.indexOf(',');
//      int motor = input.substring(0, commaIdx).toInt();
//      int direction = input.substring(commaIdx + 1).toInt();
//      stopRequested = false;
//
//      if (motor == 1) {
//        direction == 1 ? motor1_forward() : motor1_backward();
//      } else if (motor == 2) {
//        direction == 1 ? motor_forward() : motor_backward();
//      } else if (motor == 3) {
//        stepManualForward = direction == 1;
//        stepManualBackward = direction == 2;
//      }
//    } else if (!manualMode && input.indexOf(',') > 0) {
//      int firstComma = input.indexOf(',');
//      int secondComma = input.indexOf(',', firstComma + 1);
//
//      if (firstComma > 0 && secondComma > firstComma) {
//        int motor = input.substring(0, firstComma).toInt();
//        char command = input.substring(firstComma + 1, secondComma).charAt(0);
//        float value = input.substring(secondComma + 1).toFloat();
//
//        stopRequested = false;
//        if (motor == 1 && command == 'd') motor1_move(value);
//        else if (motor == 2 && command == 'd') moveDCMotorDistance(value);
//        else if (motor == 3 && command == 'a') rotateStepMotor(value);
//      }
//    }
//  }
//}
//
//void executeAutoSequence() {
//  Serial.println("[자동] 빨간 병 작업 시작");
//  motor1_move(-5.0);
//  rotateStepMotor(50.0);
//  moveDCMotorDistance(-10.0);
//  motor1_move(5.0);
//  moveDCMotorDistance(10.0);
//  rotateStepMotor(-50.0);
//  Serial.println("[자동] 빨간 병 작업 완료");
//}
//
//void rotateStepMotor(float yellowDegree) {
//  stepMotorRunning = true;
//  bool clockwise = yellowDegree >= 0;
//  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);
//
//  float motorDegree = abs(yellowDegree) * 360.0;
//  float anglePerStep = 360.0 / stepsPerRevolution;
//  long stepsToMove = round((motorDegree / 360.0) * stepsPerRevolution);
//  long actualStepsMoved = 0;
//
//  for (long i = 0; i < stepsToMove; i++) {
//    if (stopRequested) break;
//    digitalWrite(stepStepPin, HIGH);
//    delayMicroseconds(20);
//    digitalWrite(stepStepPin, LOW);
//    delayMicroseconds(20);
//    actualStepsMoved++;
//  }
//
//  float motorRotated = actualStepsMoved * anglePerStep;
//  float yellowRotated = motorRotated / 360.0;
//  yellowGearAngle += clockwise ? yellowRotated : -yellowRotated;
//
//  Serial.print("스텝모터 누적 각도: ");
//  Serial.println(yellowGearAngle);
//
//  stepMotorRunning = false;
//}
//
//void moveDCMotorDistance(float distance_cm) {
//  float angle = (distance_cm * 360.0) / ((motor_gear_diameter / second_gear_diameter) * (pi * final_gear_diameter));
//  if (distance_cm >= 0) motor_forward();
//  else motor_backward();
//  delay((unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor));
//  motor_stop();
//}
//
//void motor1_move(float distance_cm) {
//  if (distance_cm >= 0) motor1_forward();
//  else motor1_backward();
//  delay((unsigned long)(abs(distance_cm) * 300.0));
//  motor1_stop();
//}
//
//void motor_forward() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor_backward() {
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor1_forward() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, HIGH);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_backward() {
//  digitalWrite(IN3, HIGH);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_stop() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void motor_stop() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//
//void emergency_stop() {
//  stopRequested = true;
//  motor_stop();
//  motor1_stop();
//  stepMotorRunning = false;
//  Serial.println("[STOP] 긴급 정지 완료");
//}




//12:40분꺼
//// <공통 설정>
//#include <Arduino.h>
//
//// <STEP 모터 설정>
//const int stepDirPin = 12;      // 스텝모터 방향 핀
//const int stepStepPin = 11;     // 스텝모터 스텝 핀
//const float stepsPerRevolution = 3200.0; // 1/16 마이크로스텝 기준
//float yellowGearAngle = 0;
//bool stepMotorRunning = false;
//
//// <DC모터 설정>
//#define ENA 6    
//#define IN1 7
//#define IN2 8
//
//int motor_speed = 200; // PWM 속도 (0~255)
//
//// <기어 및 이동 계산 설정>
//const float motor_gear_diameter = 7.0;  // 모터 기어 지름(cm)
//const float second_gear_diameter = 4.0; // 맞물린 기어 지름(cm)
//const float final_gear_diameter = 3.0;  // 최종 체인 기어 지름(cm)
//const float pi = 3.1415;
//
//// <보정 비율 설정>
//const float distance_correction_factor = 2.7; // 이동 보정 비율 (4cm -> 10cm 맞추기 위해 2.5배)
//
//bool stopRequested = false;
//bool autoMode = false;
//bool manualMode = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//
//void setup() {
//  Serial.begin(9600);
//
//  // 스텝모터 핀 설정
//  pinMode(stepStepPin, OUTPUT);
//  pinMode(stepDirPin, OUTPUT);
//
//  // DC모터 핀 설정
//  pinMode(IN1, OUTPUT);
//  pinMode(IN2, OUTPUT);
//  pinMode(ENA, OUTPUT);
//
//  Serial.println("입력 형식: 모드(a/m), 정지(q), 또는 모터번호,명령,값");
//  Serial.println("예시) a: 자동 모드 전환");
//  Serial.println("예시) m: 수동 모드 전환");
//  Serial.println("예시) 1,d,5 : 집게팔 모터 5cm 이동");
//  Serial.println("예시) 3,a,90 : 스텝모터 90도 회전");
//  Serial.println("예시) 2,d,10 : DC모터 10cm 이동");
//  Serial.println("예시) q : 긴급 정지");
//}
//
//void loop() {
//  checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(500);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(500);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(500);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(500);
//    }
//  }
//}
//
//void checkSerialInput() {
//  if (Serial.available() > 0) {
//    String input = Serial.readStringUntil('\n');
//    input.trim();
//
//    if (input.equalsIgnoreCase("q")) {
//      stopRequested = true;
//      emergency_stop();
//    } else if (input.equalsIgnoreCase("a")) {
//      autoMode = true;
//      manualMode = false;
//      Serial.println("자동 모드 시작");
//      executeAutoSequence();
//    } else if (input.equalsIgnoreCase("m")) {
//      autoMode = false;
//      manualMode = true;
//      Serial.println("수동 모드 시작");
//    } else if (manualMode && input.indexOf(',') > 0) {
//      int commaIdx = input.indexOf(',');
//      int motor = input.substring(0, commaIdx).toInt();
//      int direction = input.substring(commaIdx + 1).toInt();
//      stopRequested = false;
//
//      if (motor == 1) {
//        direction == 1 ? motor_forward() : motor_backward();
//      } else if (motor == 2) {
//        direction == 1 ? motor_forward() : motor_backward();
//      } else if (motor == 3) {
//        stepManualForward = direction == 1;
//        stepManualBackward = direction == 2;
//      }
//    } else if (!manualMode && input.indexOf(',') > 0) {
//      int firstComma = input.indexOf(',');
//      int secondComma = input.indexOf(',', firstComma + 1);
//
//      if (firstComma > 0 && secondComma > firstComma) {
//        int motor = input.substring(0, firstComma).toInt();
//        char command = input.substring(firstComma + 1, secondComma).charAt(0);
//        float value = input.substring(secondComma + 1).toFloat();
//
//        stopRequested = false;
//        if (motor == 1 && command == 'd') moveDCMotorDistance(value);
//        else if (motor == 2 && command == 'd') moveDCMotorDistance(value);
//        else if (motor == 3 && command == 'a') rotateStepMotor(value);
//      }
//    }
//  }
//}
//
//void executeAutoSequence() {
//  // 빨간 병 인식 동작 시퀀스
//  Serial.println("[자동] 빨간 병 작업 시작");
//  moveDCMotorDistance(1.0);
//  rotateStepMotor(50.0);
//  moveDCMotorDistance(-10.0);
//  moveDCMotorDistance(-1.0);
//  moveDCMotorDistance(10.0);
//  Serial.println("[자동] 빨간 병 작업 완료");
//}
//
//void rotateStepMotor(float yellowDegree) {
//  stepMotorRunning = true;
//  bool clockwise = yellowDegree >= 0;
//  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);
//
//  float motorDegree = abs(yellowDegree) * 360.0;
//  float anglePerStep = 360.0 / stepsPerRevolution;
//  long stepsToMove = round((motorDegree / 360.0) * stepsPerRevolution);
//  long actualStepsMoved = 0;
//
//  for (long i = 0; i < stepsToMove; i++) {
//    if (stopRequested) break;
//    digitalWrite(stepStepPin, HIGH);
//    delayMicroseconds(20);
//    digitalWrite(stepStepPin, LOW);
//    delayMicroseconds(20);
//    actualStepsMoved++;
//  }
//
//  float motorRotated = actualStepsMoved * anglePerStep;
//  float yellowRotated = motorRotated / 360.0;
//  yellowGearAngle += clockwise ? yellowRotated : -yellowRotated;
//
//  Serial.print("스텝모터 누적 각도: ");
//  Serial.println(yellowGearAngle);
//
//  stepMotorRunning = false;
//}
//
//void moveDCMotorDistance(float distance_cm) {
//  float angle = (distance_cm * 360.0) / ((motor_gear_diameter / second_gear_diameter) * (pi * final_gear_diameter));
//  if (distance_cm >= 0) motor_forward();
//  else motor_backward();
//  delay((unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor));
//  motor_stop();
//}
//
//void motor_forward() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor_backward() {
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor_stop() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//
//void emergency_stop() {
//  stopRequested = true;
//  motor_stop();
//  stepMotorRunning = false;
//  Serial.println("[STOP] 긴급 정지 완료");
//}




////05.07,11:30
//// <공통 설정>
//#include <Arduino.h>
//
//// <3번 STEP 모터 설정>
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 40;
//float yellowGearAngle = 0;
//bool stepMotorRunning = false;
//
//// <2번 모터: 상하 DC 모터>
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2
//int motor_speed = 200;
//volatile long encoderCount = 0;
//
//// <1번 모터: 집게 DC 모터>
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4
//
//// <기어 및 이동 계산 설정>
//const float motor_gear_diameter = 7.0;
//const float second_gear_diameter = 4.0;
//const float final_gear_diameter = 3.0;
//const float pi = 3.1415;  
//
//// <보정 비율 설정>
//const float distance_correction_factor = 2.7;
//
//// <상태 플래그>
//bool stopRequested = false;
//bool autoMode = false;
//bool manualMode = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//
//void setup() {
//  Serial.begin(9600);
//  pinMode(stepStepPin, OUTPUT);
//  pinMode(stepDirPin, OUTPUT);
//  pinMode(IN1, OUTPUT);
//  pinMode(IN2, OUTPUT);
//  pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT);
//  pinMode(IN4, OUTPUT);
//  pinMode(ENB, OUTPUT);
//
//  Serial.println("입력 형식: 모드(a/m), 정지(q), 또는 모터번호,명령,값");
//  Serial.println("예시) a: 자동 모드 전환");
//  Serial.println("예시) m: 수동 모드 전환");
//  Serial.println("예시) 1,d,5 : 집게팔 모터 5cm 이동");
//  Serial.println("예시) 3,a,90 : 스텝모터 90도 회전");
//  Serial.println("예시) 2,d,10 : DC모터 10cm 이동");
//  Serial.println("예시) 1,1 : 집게 정방향");
//  Serial.println("예시) 1,2 : 집게 역방향");
//  Serial.println("예시) 2,1 : 집게 상승");
//  Serial.println("예시) 2,2 : 집게 하강");
//  Serial.println("예시) 3,1 : 좌회전");
//  Serial.println("예시) 3,2 : 우회전");
//  Serial.println("예시) q : 긴급 정지 (수동 모드에서만)");
//}
//
//void loop() {
//  checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(40);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(40);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(40);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(40);
//    }
//  }
//}
//
//void checkSerialInput() {
//  if (Serial.available() > 0) {
//    String input = Serial.readStringUntil('\n');
//    input.trim();
//
//    if (input.equalsIgnoreCase("q") && manualMode) {
//      stopRequested = true;
//      emergency_stop();
//    } else if (input.equalsIgnoreCase("a")) {
//      autoMode = true;
//      manualMode = false;
//      Serial.println("자동 모드 전환됨 (YOLO 제어 대기 중)");
//    } else if (input.equalsIgnoreCase("m")) {
//      autoMode = false;
//      manualMode = true;
//      Serial.println("수동 모드 시작");
//    } else if (input.indexOf(',') > 0) {
//      int comma = input.indexOf(',');
//      String first = input.substring(0, comma);
//      String second = input.substring(comma + 1);
//
//      // 단축 명령 처리
//      if (second.length() == 1) {
//        int motor = first.toInt();
//        int action = second.toInt();
//
//        if (manualMode) {
//          stopRequested = false;
//          stepManualForward = false;
//          stepManualBackward = false;
//
//          if (motor == 1 && action == 1) motor1_forward();
//          else if (motor == 1 && action == 2) motor1_backward();
//          else if (motor == 2 && action == 1) motor2_backward();  // 상승
//          else if (motor == 2 && action == 2) motor2_forward();   // 하강
//          else if (motor == 3 && action == 1) stepManualBackward = true;
//          else if (motor == 3 && action == 2) stepManualForward = true;
//        }
//      }
//      // 기존 포맷 처리
//      else {
//        int firstComma = input.indexOf(',');
//        int secondComma = input.indexOf(',', firstComma + 1);
//
//        if (firstComma > 0 && secondComma > firstComma) {
//          int motor = input.substring(0, firstComma).toInt();
//          char command = input.substring(firstComma + 1, secondComma).charAt(0);
//          float value = input.substring(secondComma + 1).toFloat();
//
//          stopRequested = false;
//
//          if (motor == 1 && command == 'd') motor1_move(value);
//          else if (motor == 2 && command == 'd') motor2_move(value);
//          else if (motor == 3 && command == 'a') rotateStepMotor(value);
//        }
//      }
//    }
//  }
//}
//
//void rotateStepMotor(float yellowDegree) {
//  stepMotorRunning = true;
//  bool clockwise = yellowDegree >= 0;
//  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);
//
//  float motorDegree = abs(yellowDegree) * 360.0;
//  float anglePerStep = 360.0 / stepsPerRevolution;
//  const float stepCorrectionFactor = 1.1;
//  long stepsToMove = round((motorDegree / 360.0) * stepsPerRevolution);
//  long actualStepsMoved = 0;
//
//  for (long i = 0; i < stepsToMove; i++) {
//    if (stopRequested) break;
//    digitalWrite(stepStepPin, HIGH);
//    delayMicroseconds(stepDelayMicros);
//    digitalWrite(stepStepPin, LOW);
//    delayMicroseconds(stepDelayMicros);
//    actualStepsMoved++;
//  }
//
//  float motorRotated = actualStepsMoved * anglePerStep;
//  float yellowRotated = motorRotated / 360.0;
//  yellowGearAngle += clockwise ? yellowRotated : -yellowRotated;
//
//  Serial.print("스텝모터 누적 각도: ");
//  Serial.println(yellowGearAngle);
//
//  stepMotorRunning = false;
//}
//
//void motor1_move(float distance_cm) {
//  if (distance_cm >= 0) motor1_forward();
//  else motor1_backward();
//  delay((unsigned long)(abs(distance_cm) * 300.0));
//  motor1_stop();
//}
//
//void motor2_move(float distance_cm) {
//  float angle = (distance_cm * 360.0) / ((motor_gear_diameter / second_gear_diameter) * (pi * final_gear_diameter));
//  if (distance_cm >= 0) motor2_forward();
//  else motor2_backward();
//  delay((unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor));
//  motor2_stop();
//}
//
//void motor1_forward() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, HIGH);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_backward() {
//  digitalWrite(IN3, HIGH);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_stop() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void motor2_forward() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor2_backward() {
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor2_stop() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//
//void emergency_stop() {
//  stopRequested = true;
//  motor1_stop();
//  motor2_stop();
//  stepManualForward = false;
//  stepManualBackward = false;
//  stepMotorRunning = false;
//  Serial.println("[STOP] 긴급 정지 완료");
//}




//되는거! 05.0, 12:57
//// <공통 설정>
//#include <Arduino.h>
//#include <math.h>
//
//// <3번 STEP 모터 설정>
//const int stepDirPin = 12;
//const int stepStepPin = 11;
//const float stepsPerRevolution = 3200.0;
//const int stepDelayMicros = 20;
//float yellowGearAngle = 0;
//bool stepMotorRunning = false;
//
//// <2번 모터: 상하 DC 모터>
//#define ENA 6
//#define IN1 7
//#define IN2 8
//#define ENCODER_2 2
//int motor_speed = 190;
//volatile long encoderCount = 0;
//
//// <1번 모터: 집게 DC 모터>
//#define ENB 3
//#define IN3 9
//#define IN4 10
//#define ENCODER_1 4
//
//// <기어 및 이동 계산 설정>
//const float motor_gear_diameter = 7.0;
//const float second_gear_diameter = 4.0;
//const float final_gear_diameter = 3.0;
//const float pi = 3.1415;
//
//// <보정 비율 설정>
//const float distance_correction_factor = 3.0;
//
//// <상태 플래그>
//bool stopRequested = false;
//bool autoMode = false;
//bool manualMode = false;
//bool stepManualForward = false;
//bool stepManualBackward = false;
//
//void setup() {
//  Serial.begin(9600);
//  pinMode(stepStepPin, OUTPUT);
//  pinMode(stepDirPin, OUTPUT);
//  pinMode(IN1, OUTPUT);
//  pinMode(IN2, OUTPUT);
//  pinMode(ENA, OUTPUT);
//  pinMode(IN3, OUTPUT);
//  pinMode(IN4, OUTPUT);
//  pinMode(ENB, OUTPUT);
//
//  Serial.println("입력 형식: 모드(a/m), 정지(q), 또는 모터번호,명령,값");
//  Serial.println("예시) a: 자동 모드 전환");
//  Serial.println("예시) m: 수동 모드 전환");
//  Serial.println("예시) 1,d,5 : 집게팔 모터 5cm 이동");
//  Serial.println("예시) 3,a,90 : 스텝모터 90도 회전");
//  Serial.println("예시) 2,d,10 : DC모터 10cm 이동");
//  Serial.println("예시) 1,1 : 집게 정방향");
//  Serial.println("예시) 1,2 : 집게 역방향");
//  Serial.println("예시) 2,1 : 집게 상승");
//  Serial.println("예시) 2,2 : 집게 하강");
//  Serial.println("예시) 3,1 : 좌회전");
//  Serial.println("예시) 3,2 : 우회전");
//  Serial.println("예시) q : 긴급 정지 (수동 모드에서만)");
//}
//
//void loop() {
//  checkSerialInput();
//
//  if (manualMode && !stopRequested) {
//    if (stepManualForward) {
//      digitalWrite(stepDirPin, HIGH);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(40);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(40);
//    } else if (stepManualBackward) {
//      digitalWrite(stepDirPin, LOW);
//      digitalWrite(stepStepPin, HIGH);
//      delayMicroseconds(40);
//      digitalWrite(stepStepPin, LOW);
//      delayMicroseconds(40);
//    }
//  }
//}
//
//void checkSerialInput() {
//  if (Serial.available() > 0) {
//    String input = Serial.readStringUntil('\n');
//    input.trim();
//
//    if (input.equalsIgnoreCase("q") && manualMode) {
//      stopRequested = true;
//      emergency_stop();
//    } else if (input.equalsIgnoreCase("a")) {
//      autoMode = true;
//      manualMode = false;
//      Serial.println("자동 모드 전환됨 (YOLO 제어 대기 중)");
//    } else if (input.equalsIgnoreCase("m")) {
//      autoMode = false;
//      manualMode = true;
//      Serial.println("수동 모드 시작");
//    } else if (input.indexOf(',') > 0) {
//      int comma = input.indexOf(',');
//      String first = input.substring(0, comma);
//      String second = input.substring(comma + 1);
//
//      if (second.length() == 1) {
//        int motor = first.toInt();
//        int action = second.toInt();
//
//        if (manualMode) {
//          stopRequested = false;
//          stepManualForward = false;
//          stepManualBackward = false;
//
//          if (motor == 1 && action == 1) motor1_forward();
//          else if (motor == 1 && action == 2) motor1_backward();
//          else if (motor == 2 && action == 1) motor2_backward();  // 상승
//          else if (motor == 2 && action == 2) motor2_forward();   // 하강
//          else if (motor == 3 && action == 1) stepManualBackward = true;
//          else if (motor == 3 && action == 2) stepManualForward = true;
//        }
//      } else {
//        int firstComma = input.indexOf(',');
//        int secondComma = input.indexOf(',', firstComma + 1);
//
//        if (firstComma > 0 && secondComma > firstComma) {
//          int motor = input.substring(0, firstComma).toInt();
//          char command = input.substring(firstComma + 1, secondComma).charAt(0);
//          float value = input.substring(secondComma + 1).toFloat();
//
//          stopRequested = false;
//
//          if (motor == 1 && command == 'd') motor1_move(value);
//          else if (motor == 2 && command == 'd') motor2_move(value);
//          else if (motor == 3 && command == 'a') rotateStepMotor(value);
//        }
//      }
//    }
//  }
//}
//
//void rotateStepMotor(float yellowDegree) {
//  stepMotorRunning = true;
//  bool clockwise = yellowDegree >= 0;
//  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);
//
//  // 1. 목표 각도 -> 목표 회전 각도 보정 (1.1배) + 스텝 보정(1.05배)
//  float motorDegree = abs(yellowDegree) * 360.0 * 1.055;
//  float anglePerStep = 360.0 / stepsPerRevolution;
//  long stepsToMove = round((motorDegree / 360.0) * stepsPerRevolution*1.07);
//
//  // 2. 감속 구간: 마지막 3%로 축소
//  long decelSteps = max(stepsToMove * 0.03, 3);
//  long fastSteps = stepsToMove - decelSteps;
//
//  // 3. 감속 딜레이 범위 축소 (빠르게 감속)
//  const int minDelay = 20;   // 빠를 때
//  const int maxDelay = 300;  // 감속 끝
//
//  for (long i = 0; i < stepsToMove; i++) {
//    if (stopRequested) break;
//
//    int delayMicrosValue = minDelay;
//
//    if (i >= fastSteps) {
//      long decelIndex = i - fastSteps;
//      float ratio = (float)decelIndex / (float)decelSteps;
//      float cosineValue = (1 - cos(ratio * PI)) / 2.0;
//      delayMicrosValue = minDelay + (int)((maxDelay - minDelay) * cosineValue);
//    }
//
//    digitalWrite(stepStepPin, HIGH);
//    delayMicroseconds(delayMicrosValue);
//    digitalWrite(stepStepPin, LOW);
//    delayMicroseconds(delayMicrosValue);
//  }
//
//  // 4. 실제 회전량 계산 (보정 포함)
//  float motorRotated = stepsToMove * anglePerStep;
//  float yellowRotated = motorRotated / 360.0;
//  yellowGearAngle += clockwise ? yellowRotated : -yellowRotated;
//
//  Serial.print("스텝모터 누적 각도: ");
//  Serial.println(yellowGearAngle);
//
//  stepMotorRunning = false;
//}
//
//
//void motor1_move(float distance_cm) {
//  if (distance_cm >= 0) motor1_forward();
//  else motor1_backward();
//  delay((unsigned long)(abs(distance_cm) * 300.0));
//  motor1_stop();
//}
//
//void motor2_move(float distance_cm) {
//  float angle = (distance_cm * 360.0) / ((motor_gear_diameter / second_gear_diameter) * (pi * final_gear_diameter));
//  if (distance_cm >= 0) motor2_forward();
//  else motor2_backward();
//  delay((unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor));
//  motor2_stop();
//}
//
//void motor1_forward() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, HIGH);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_backward() {
//  digitalWrite(IN3, HIGH);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, motor_speed);
//}
//
//void motor1_stop() {
//  digitalWrite(IN3, LOW);
//  digitalWrite(IN4, LOW);
//  analogWrite(ENB, 0);
//}
//
//void motor2_forward() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, HIGH);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor2_backward() {
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, motor_speed);
//}
//
//void motor2_stop() {
//  digitalWrite(IN1, LOW);
//  digitalWrite(IN2, LOW);
//  analogWrite(ENA, 0);
//}
//
//void emergency_stop() {
//  stopRequested = true;
//  motor1_stop();
//  motor2_stop();
//  stepManualForward = false;
//  stepManualBackward = false;
//  stepMotorRunning = false;
//  Serial.println("[STOP] 긴급 정지 완료");
//}




// <공통 설정>
#include <Arduino.h>
#include <math.h>

// <3번 STEP 모터 설정>
const int stepDirPin = 12;
const int stepStepPin = 11;
const float stepsPerRevolution = 3200.0;
const int stepDelayMicros = 20;
float yellowGearAngle = 0;
bool stepMotorRunning = false;

// <2번 모터: 상하 DC 모터>
#define ENA 6
#define IN1 7
#define IN2 8
#define ENCODER_2 2
int motor_speed = 190;
volatile long encoderCount = 0;

// <1번 모터: 집게 DC 모터>
#define ENB 3
#define IN3 9
#define IN4 10
#define ENCODER_1 4

// <기어 및 이동 계산 설정>
const float motor_gear_diameter = 7.0;
const float second_gear_diameter = 4.0;
const float final_gear_diameter = 3.0;
const float pi = 3.1415;

// <보정 비율 설정>
const float distance_correction_factor = 3.0;

// <상태 플래그>
bool stopRequested = false;
bool autoMode = false;
bool manualMode = false;
bool stepManualForward = false;
bool stepManualBackward = false;

void setup() {
  Serial.begin(9600);
  pinMode(stepStepPin, OUTPUT);
  pinMode(stepDirPin, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.println("입력 형식: 모드(a/m), 정지(q), 또는 모터번호,명령,값");
  Serial.println("예시) a: 자동 모드 전환");
  Serial.println("예시) m: 수동 모드 전환");
  Serial.println("예시) 1,d,5 : 집게팔 모터 5cm 이동");
  Serial.println("예시) 3,a,90 : 스텝모터 90도 회전");
  Serial.println("예시) 2,d,10 : DC모터 10cm 이동");
  Serial.println("예시) 1,1 : 집게 정방향");
  Serial.println("예시) 1,2 : 집게 역방향");
  Serial.println("예시) 2,1 : 집게 상승");
  Serial.println("예시) 2,2 : 집게 하강");
  Serial.println("예시) 3,1 : 좌회전");
  Serial.println("예시) 3,2 : 우회전");
  Serial.println("예시) q : 긴급 정지 (수동 모드에서만)");
}

void loop() {
  checkSerialInput();

  if (manualMode && !stopRequested) {
    if (stepManualForward) {
      digitalWrite(stepDirPin, HIGH);
      digitalWrite(stepStepPin, HIGH);
      delayMicroseconds(40);
      digitalWrite(stepStepPin, LOW);
      delayMicroseconds(40);
    } else if (stepManualBackward) {
      digitalWrite(stepDirPin, LOW);
      digitalWrite(stepStepPin, HIGH);
      delayMicroseconds(40);
      digitalWrite(stepStepPin, LOW);
      delayMicroseconds(40);
    }
  }
}

void checkSerialInput() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("q") && manualMode) {
      stopRequested = true;
      emergency_stop();
    } else if (input.equalsIgnoreCase("a")) {
      autoMode = true;
      manualMode = false;
      Serial.println("자동 모드 전환됨 (YOLO 제어 대기 중)");
    } else if (input.equalsIgnoreCase("m")) {
      autoMode = false;
      manualMode = true;
      Serial.println("수동 모드 시작");
    } else if (input.indexOf(',') > 0) {
      int comma = input.indexOf(',');
      String first = input.substring(0, comma);
      String second = input.substring(comma + 1);

      if (second.length() == 1) {
        int motor = first.toInt();
        int action = second.toInt();

        if (manualMode) {
          stopRequested = false;
          stepManualForward = false;
          stepManualBackward = false;

          if (motor == 1 && action == 1) motor1_forward();
          else if (motor == 1 && action == 2) motor1_backward();
          else if (motor == 2 && action == 1) motor2_backward();  // 상승
          else if (motor == 2 && action == 2) motor2_forward();   // 하강
          else if (motor == 3 && action == 1) stepManualBackward = true;
          else if (motor == 3 && action == 2) stepManualForward = true;
        }
      } else {
        int firstComma = input.indexOf(',');
        int secondComma = input.indexOf(',', firstComma + 1);

        if (firstComma > 0 && secondComma > firstComma) {
          int motor = input.substring(0, firstComma).toInt();
          char command = input.substring(firstComma + 1, secondComma).charAt(0);
          float value = input.substring(secondComma + 1).toFloat();

          stopRequested = false;

          if (motor == 1 && command == 'd') motor1_move(value);
          else if (motor == 2 && command == 'd') motor2_move(value);
          else if (motor == 3 && command == 'a') rotateStepMotor(value);
        }
      }
    }
  }
}

void rotateStepMotor(float yellowDegree) {
  stepMotorRunning = true;
  bool clockwise = yellowDegree >= 0;
  digitalWrite(stepDirPin, clockwise ? HIGH : LOW);

  float targetYellowAngle = abs(yellowDegree); // 도 단위

  float anglePerStep = 360.0 / stepsPerRevolution;
  long stepsToMove = round((targetYellowAngle / anglePerStep) * 1.2); // 스텝 수만 소폭 보정

  long decelSteps = max(stepsToMove * 0.03, 3); // 마지막 3% 감속
  long fastSteps = stepsToMove - decelSteps;

  const int minDelay = 20;
  const int maxDelay = 400;

  for (long i = 0; i < stepsToMove; i++) {
    if (stopRequested) break;

    int delayMicrosValue = minDelay;

    if (i >= fastSteps) {
      long decelIndex = i - fastSteps;
      float ratio = (float)decelIndex / (float)decelSteps;
      float cosineValue = (1 - cos(ratio * pi)) / 2.0;
      delayMicrosValue = minDelay + (int)((maxDelay - minDelay) * cosineValue);
    }

    digitalWrite(stepStepPin, HIGH);
    delayMicroseconds(delayMicrosValue);
    digitalWrite(stepStepPin, LOW);
    delayMicroseconds(delayMicrosValue);
  }

  yellowGearAngle += clockwise ? targetYellowAngle : -targetYellowAngle;

  Serial.print("스텝모터 누적 각도: ");
  Serial.println(yellowGearAngle);

  stepMotorRunning = false;
}

void motor1_move(float distance_cm) {
  if (distance_cm >= 0) motor1_forward();
  else motor1_backward();
  delay((unsigned long)(abs(distance_cm) * 300.0));
  motor1_stop();
}

void motor2_move(float distance_cm) {
  float angle = (distance_cm * 360.0) / ((motor_gear_diameter / second_gear_diameter) * (pi * final_gear_diameter));
  if (distance_cm >= 0) motor2_forward();
  else motor2_backward();
  delay((unsigned long)(abs(angle) * 3000.0 / 360.0 * distance_correction_factor));
  motor2_stop();
}

void motor1_forward() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, motor_speed);
}

void motor1_backward() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, motor_speed);
}

void motor1_stop() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}

void motor2_forward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, motor_speed);
}

void motor2_backward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, motor_speed);
}

void motor2_stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}

void emergency_stop() {
  stopRequested = true;
  motor1_stop();
  motor2_stop();
  stepManualForward = false;
  stepManualBackward = false;
  stepMotorRunning = false;
  Serial.println("[STOP] 긴급 정지 완료");
}
