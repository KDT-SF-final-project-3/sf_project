# 🦾스마트 팩토리 눈과 손 : Web-based 실시간 모니터링 & Robot Arm Control
## 1. 프로젝트 개요 및 주제 선정 배경
- 프로젝트 목표
 
- 주제 선정 이유
  - 스마트 팩토리 필요성 증가.
  - 생산성 향상 및 공정 자동화 기술 향상.
    
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
| 이름     | 역할           | 주요 업무                                                                                              |
|----------|----------------|----------------------------------------------------------------------------------------------------------|
| 유승태   | 팀장, SW 담당   | **프로젝트 기획**, 일정 조율 및 감독, 기초 서버 담당, 발표 자료 수집, 발표  <br> - **Back-end**: DB 모델 설계 및 Server 연결, OpenCV-Server 연결 <br> - **Front-end**: 실시간 로봇팔 모니터링 및 제어 기능, 제어 이력 및 현황 출력 기능 제작 <br> - **HW 연동**: Server를 통해 연결된 HW와 DB를 이용하여 센서 데이터를 MySQL 저장 | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/Yoo-Seung-Tae) |
| 한용찬   | 팀원, HW 담당   | **프로젝트 기획**, 로봇팔 시스템 담당, 발표 자료 수집 <br> - **HW**: 상하 제어 DC 모터, 집게팔 제어 DC 모터 아두이노 회로 구현, 모터 선정 및 제어, 센서 제어 <br> - **SW**: 아두이노 기반 제어 기능 코딩, DB-기능서버 연동                                | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/gksdydcks) |
| 황세진   | 팀원, HW 담당   | **프로젝트 기획**, 로봇팔 시스템 담당, 발표 자료 수집 <br> - **HW**: 회전 제어 스텝 모터, 집게팔 제어 DC모터 아두이노 회로 구현, 모터 선정 및 제어, 센서 제어 <br> - **SW**: 아두이노 기반 제어 기능 코딩, DB-기능서버 연동                                | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/sejin1048)|
| 김희수   | 팀원, SW 담당   | **프로젝트 기획**, 메인 서버 담당, 발표 자료 제작 <br> - **Back-end**: 서버 환경 구축, DB 모델 설계 및 Server 연결, Django-React (axios 통신) 연결 <br> - **Front-end**: React를 활용한 웹사이트 구축, 로그인 & 회원가입 기능 제작                      | [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)]() |


## 4. 개발 일정
| 마일스톤 | 목표 날짜           | 설명                                               |
|----------|--------------------|----------------------------------------------------|
| 사전 기획 | 2025-03-19         | 프로젝트 기획, 주제 선정, git 생성                |
| 아두이노, 웹캠 연결 | 2025-03-19 ~ 03-20 | 아두이노-PC 연결, MFC GUI 구상, 웹캠 연결        |
| AI, 로봇팔 작동 기능 구현 | 2025-03-21         | openCV에 yolo 탑재, 로봇팔 작동 버튼 및 기능 구현 |
| AI적용 로봇팔 기능 추가 | 2025-03-22 ~ 03-24 | 인식된 객체에 따른 각각 다른 동작 기능 추가      |
| 오류 수정 | 2025-03-25 ~ 03-26 | 오류 수정 및 정리                                 |
| 시연     | 2025-03-27         | 프로젝트 시연                                     |
  
## 5. 개발 프로세스

- 개발 순서
  
 
     
  
- 플로우 차트
  


- 핵심 기능 리스트

  | 기능 이름 | 설명 | 우선순위 | 담당자 |
  | --- | --- | --- | --- |
  | MFC 화면 출력 | MFC 기반 GUI 출력 | medium | 유승태, 한용찬 |
  | X축 이동 | 로봇 팔을 위, 아래로 이동 | High | 유승태, 한용찬 |
  | 집게 조작 | 조작을 통한 물건 잡기 및 놓기 | High | 유승태, 한용찬 |
  | 웹캠 연결 | 작업 현장 확인 및 이미지 입력 | medium | 유승태, 한용찬 |
  | 정지 | 모든 기능 즉시 정지 | Low | 유승태, 한용찬 |
  | AI 기능 구현 | 객체 인식하여 인식된 객체에 따른 자동 운행 | high | 유승태, 한용찬 |
  
- 시스템 구성
  
## 8. 한계점 및 추후 착안 사항
- 하드웨어 제작 리소스 및 경험 부족에 따른 기능 추가 및 고도화에 한계가 있었음.
    - 시간으로 모터를 통제했는데, 그때마다 움직임에 오차가 발생함. 추가적인 센서를 통해서 이중 통제가 필요함.
    - 또한, 모터의 힘과 정밀성의 부족함에 따라 정밀한 움직임 구현에 한계가 있었음.
    - 추후 자금 확보 및 리소스 확보가 가능하다면 충분히 더 좋은 결과를 낼 수 있음.
- C++ 특성상 라이브러리 사용이 복잡하여 개발에 어려움이 있었음.
    - 이번 프로젝트는 C++에서 OpenCV와 Yolo를 사용하였고, 파이썬으로 개발하는 것이 효율적이라고 생각함.
    - 파이썬으로 기능을 구현하고 C++로 구현하는 방법이 효율적이라고 판단함.

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



