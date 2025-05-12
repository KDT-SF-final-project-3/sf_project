# 🦾스마트 팩토리 눈과 손 : Web-based 실시간 모니터링 & Robot Arm Control
## 1. 프로젝트 개요
### 프로젝트 목표
- 아두이노와 각종 센서 및 모터를 사용하여 HW(로봇팔)를 제작하고, 파이썬 기반의 서버를 구현하여 스마트팩토리에서 활용하는 통합 관제 시스템을 구축
### 프로잭트 목적
- 아두이노를 사용하여 로봇팔을 제어하고, 공장에서 활용되는 환경을 **프로토타입 형태**로 구현하고자 함
- 스마트팩토리에서 운용되는 **통합 서버 시스템**을 직접 구축하고자 함
- **DB와의 연동**을 통해 시스템 운영 중 생성되는 데이터를 저장하고자 함
### 주제 선정 이유
  - 스마트 팩토리 필요성 증가.
  - 생산성 향상 및 공정 자동화 기술 향상.
### 주요 기능
- 객체 인식 기능을 통해 로봇팔을 제어하며, 객체의 종류에 따라 구분된 동작을 구현함
- 로봇의 동작 이력 및 센서로 수집한 환경 정보를 DB에 저장하고, 실시간으로 웹페이지를 통해 확인 가능함


## 2. 주요 기술 스택
<table>
  <tr>
    <th>카테고리</th>
    <th>기술 및 버전</th>
    <th>협업 툴</th>
  </tr>
  <tr>
    <td>언어</td>
    <td>Python 3.13, SQL, CSS3, JavaScript(ES6), React 19.1.0</td>
    <td rowspan="5">
      kakaoTalk (연락)<br>
      Discord (비대면 회의)<br>
      Notion (문서 정리)<br>
      Git / Github (코드 정리)
    </td>
  </tr>
  <tr>
    <td>프레임워크/데이터베이스</td>
    <td>
      Django 5.2<br>
      - djangorestframework 3.16.0 (API)<br>
      - djangorestframework_simplejwt 5.5.0 (API token 활용)
    </td>
  </tr>
  <tr>
    <td>프론트엔드 라이브러리</td>
    <td>
      React Router DOM 7.5.3, Axios 1.8.4 (서버 통신), JWT Decode 4.0.0<br>
      Ant Design (antd) 5.24.9, Styled Components 6.1.17 (CSS 디자인)
    </td>
  </tr>
  <tr>
    <td>알고리즘 / AI</td>
    <td>OpenCV(영상처리), YOLOv8 (객체 인식)</td>
  </tr>
  <tr>
    <td>도구</td>
    <td>Visual Studio Code, Arduino IDE 2.3.6, fritzing - 1.0.5 (회로도 작성)</td>
  </tr>
</table>


## 3. 팀 구성 및 역할 분담
| 이름     | 역할           | 주요 업무                                                                                              |깃허브 주소       |
|----------|----------------|----------------------------------------------------------------------------------------------------------|--------|
| 유승태   | 팀장, SW 담당   | **프로젝트 기획**, 일정 조율 및 감독, 기초 서버 담당, 발표 자료 수집, 발표  <br> - **Back-end**: DB 모델 설계 및 Server 연결, OpenCV-Server 연결 <br> - **Front-end**: 실시간 로봇팔 모니터링 및 제어 기능, 제어 이력 및 현황 출력 기능 제작 <br> - **HW 연동**: Server를 통해 연결된 HW와 DB를 이용하여 센서 데이터를 MySQL 저장 | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/Yoo-Seung-Tae) |
| 한용찬   | 팀원, HW 담당   | **프로젝트 기획**, 로봇팔 시스템 담당, 발표 자료 수집 <br> - **HW**: 상하 제어 DC 모터, 집게팔 제어 DC 모터 아두이노 회로 구현, 모터 선정 및 제어, 센서 제어 <br> - **SW**: 아두이노 기반 제어 기능 코딩, DB-기능서버 연동                                | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/gksdydcks) |
| 황세진   | 팀원, HW 담당   | **프로젝트 기획**, 로봇팔 시스템 담당, 발표 자료 수집 <br> - **HW**: 회전 제어 스텝 모터, 집게팔 제어 DC모터 아두이노 회로 구현, 모터 선정 및 제어, 센서 제어 <br> - **SW**: 아두이노 기반 제어 기능 코딩, DB-기능서버 연동                                | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/sejin1048)|
| 김희수   | 팀원, SW 담당   | **프로젝트 기획**, 메인 서버 담당, 발표 자료 제작 <br> - **Back-end**: 서버 환경 구축, DB 모델 설계 및 Server 연결, Django-React (axios 통신) 연결 <br> - **Front-end**: React를 활용한 웹사이트 구축, 로그인 & 회원가입 기능 제작                      | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/BunnyByee) |


## 4. 개발 일정

| 마일스톤             | 목표 날짜                      | 세부 설명                                                                 |
|----------------------|-------------------------------|--------------------------------------------------------------------------|
| 프로젝트 기획        | 2025-04-14 ~ 2025-04-15       | 주제 선정 및 프로젝트 계획서 작성                                           |
| 자료 수집            | 2025-04-14 ~ 2025-04-16       | 자료 수집 및 분석 후, 시퀀스별 타임 차트 작성                                 |
| 프로젝트 계획서 발표 | 2025-04-16                    | 프로젝트 계획서 발표                                                        |
| 1차 기능 구현        | 2025-04-16 ~ 2025-04-25       | - **Back-end**: 서버 환경 구축 및 DB 설계  <br> - **Front-end**: 기본 UI 블록 구성  <br> - **HW**: 필요한 센서 및 모터 테스트 |
| 중간 점검            | 2025-04-26                    | 팀원별 1차 피드백 확인 및 기능 추가 회의                                     |
| 피드백 수용          | 2025-04-26 ~ 2025-04-28       | 피드백 수용 및 추가 기능 추가                                               |
| 1차 완성 목표        | 2025-04-28                    | 모든 기능 구현 완료 <br> - DB / Server 연동 완료 <br> - 웹 페이지 기본 구조 완성 <br> - 하드웨어 초기 세팅 완료 |
| 오류 수정 및 발표 준비 | 2025-04-28 ~ 2025-05-09       | - DB / HW 연동 완료  <br> - Front / HW 연동 구현  <br> - 전체 시스템 통합 테스트  <br> - 최종 PPT 자료 작성 및 발표 대본 작성, 발표 연습 |
| 최종 프로젝트 발표   | 2025-05-09                    | 최종 프로젝트 발표!           
  
## 5. 개발 프로세스


 
     
  
- 플로우 차트
  
![Image](https://github.com/user-attachments/assets/1fdf2a59-9cd5-406d-81c2-124ece835864)

- 핵심 기능 리스트
 
| 기능 번호 | 주요 기능                | 설명                                                         | 담당자             | 중요도 |
|-----------|--------------------------|--------------------------------------------------------------|--------------------|--------|
| 1-1.1     | 서버 환경 생성           | 백엔드(메인 서버) 만들기 – 필요한 파일 생성 및 GitHub에 업로드 | 김희수, 유승태             | High   |
| 1-1.2     | 로그인 기능              | 회원가입, 로그인 기능 구현 및 권한에 따른 승인 가입 처리        | 김희수                  | Medium |
| 1-2.1     | 아두이노 DB 생성         | DB 설계: 온도, 습도 등 센서 데이터 저장                          | 유승태             | Low    |
| 1-2.2     | 회원가입 DB 생성         | 회원정보(DB) 설계: 이름, 아이디, 비밀번호, 권한 등               | 김희수             | Low    |
| 1-3       | main = Front 연동        | React 서버 생성 및 메인서버 연결                               | 김희수             | High   |
| 1-4.1     | Server = DB 연동(회원가입) | MySQL 연동 및 데이터베이스 연결 확인                            | 김희수             | Low   |
| 1-4.2     | Server = DB 연동(아두이노) | MySQL 연동, 아두이노 데이터 저장 함수 작성                       | 유승태, 한용찬, 황세진      | Low    |
| 1-5       | Server = HW 연동         | 시리얼 통신으로 아두이노(uno) 2개 연결                         | 유승태             | High    |
| 1-6       | Front = HW 연동          | React → 서버 → 아두이노 제어 및 동작 확인                       | 유승태,한용찬, 황세진      | High   |
| 1-7       | 웹캠 연동                | 웹캠 → 아두이노 연결, react에 출력                             |  유승태            | Medium |
| 1-8       | 페이지 구조화            | 퀴즈 및 안내 페이지, 웹캠 연결 페이지 구성                       | 유승태 ,김희수           | Medium |
| 2-1       | HW 동작                 | 3개 모터 상하작동 및 집게팔 동작                               | 한용찬, 황세진      | High   |
| 2-2       | 온습도 측정              | DB에 저장 후 화면에 온도, 습도 표시                            | 한용찬,황세진           | Medium |
| 2-3       | 팬 모터 작동             | 습도 60 이상시 팬 작동                                       | 한용찬, 황세진             | Medium |
| 2-4       | 조명 조절                | 조도 센서 값에 따라 LED ON/OFF 제어                          | 한용찬, 황세진             | Medium |
| 2-5       | 객체 인식                | 웹캠으로 객체 인식 후 동작 및 DB 저장                          | 한용찬, 황세진      | High   |


  
- 시스템 구성
- 

## 6.SW

## 7,HW

  
## 8. 한계점 및 추후 착안 사항 (트러블 슈팅)
- 하드웨어 제작 리소스 및 경험 부족에 따른 기능 추가 및 고도화에 한계가 있었음.
    - 시간으로 모터를 통제했는데, 그때마다 움직임에 오차가 발생함. 추가적인 센서를 통해서 이중 통제가 필요함.
    - 또한, 모터의 힘과 정밀성의 부족함에 따라 정밀한 움직임 구현에 한계가 있었음.
    - 추후 자금 확보 및 리소스 확보가 가능하다면 충분히 더 좋은 결과를 낼 수 있음.
- C++ 특성상 라이브러리 사용이 복잡하여 개발에 어려움이 있었음.
    - 이번 프로젝트는 C++에서 OpenCV와 Yolo를 사용하였고, 파이썬으로 개발하는 것이 효율적이라고 생각함.
    - 파이썬으로 기능을 구현하고 C++로 구현하는 방법이 효율적이라고 판단함.

##


## 9. 참고 자료 및 링크

### 주제 선정 배경

- 현대차그룹 - https://biz.heraldcorp.com/article/10451582?ref=naver
- 한화에어로스페이스 - https://biz.heraldcorp.com/article/10447034?ref=naver
- 독일 지멘스 - https://www.hankyung.com/article/2022091248781
- 삼성전자 - https://www.fnnews.com/news/202403311808261099

### 소프트웨어 부분

- Django 공식 홈페이지 - https://www.djangoproject.com/
- Node.js 홈페이지 - https://nodejs.org/en/download/
- Django - React 연동 - https://oliopasta.tistory.com/11
- pip 홈페이지 - https://pypi.org/project/mysqlclient/

### 하드웨어 부분

- 17hS8401 / 스텝모터 회로도 - https://blog.naver.com/roboholic84/222406097514
- 스텝 모터 연결 - https://www.makerguides.com/tb6600-stepper-motor-driver-arduino-tutorial/
- JGA25 상하, 집게팔 제어 DC모터 & L298N 듀얼모터 드라이브 회로도 - https://bota.tistory.com/2329
- CDS모듈 회로도 - https://blog.naver.com/eduino/222064604122
- 팬 모터 모듈 회로도 - https://blog.naver.com/roboholic84/220537814504
- LED(G)LED 회로도 - https://m.blog.naver.com/dong000811/222583342016
- DHT11 회로도 - https://blog.naver.com/boilmint7/220928870337

### fzpz파일 : Fritzing 부품 파일
- TB6600 스텝 모터 드라이버 .fzpz파일 - https://forum.fritzing.org/t/where-can-i-get-tb6600-v1-2-parts/17237
- 엔코더DC모터 .fzpz파일 - https://forum.fritzing.org/t/dc-motor-with-two-phase-encoder/3776/2
- L298n모터 드라이브 .fzpz파일 – https://forum.fritzing.org/t/h-bridge-with-l298n-motor-driver/7711
- 조도센서 모듈 .fzpz파일 - https://arduinomodules.info/download/ky-018-photoresistor-module-zip-file/
- 팬모터 .fzpz파일 - https://forum.fritzing.org/t/l9110-h-bridge-module/3110



