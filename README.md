# Danbi 교육 과제 🔥

## ***Introduction*** ✔

- 윙크 서비스 내에 Routine 기능을 추가하고자 합니다.
- Routine 기능이란, 매 주마다 정해진 일정에 자신이 해야할 일을 등록하고, 해당 수행여부에 대한 내용을 기록하여 관리할 수 있도록 도와주는 기능입니다.
- Routine 기능에서는 다음과 같은 기능을 제공하고자 합니다.
    - 유저의 로그인/로그아웃 기능
    - 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능
    - 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록
        - 각 할일에 대한 결과는 독립된 결과로 기록되어야 함
        - 예시)월/수/금 할일로 등록했을 때, 특정 날짜 데이터를 조회하면 조회한 날짜에 대한 수행결과만 모두 조회가 되도록 구성

### ***Summary*** 🔽
> - Project 소개
>   - 루틴, 루틴 결과 CRUD 구현
>   - 카카오 Map API를 이용하여 지역 게시판과 연동
>   - DjangoRestFramework를 이용하여 회원, 루틴 정보 저장용 REST API 서버 구현
>   - JWT를 이용하여 OAuth 2.0 Auth 프로토콜 기반으로 Authentication 및 Authorization 구현


### ***Requirments*** 🤔
> - BACKEND(Djagno Authentication Server)
>   - django~=3.0.0
>   - djangorestframework~=3.11.0
>   - djangorestframework-simplejwt
>   - mysqlclient

> - DataBase
>   - MySQL

<br>

### ***IDE*** 🥢
> - BACKEND
>   - Pycharm Professional
>   - VScode
>   - Postman
>   - MySQL Workbench


<br>

### ***Backend End-points*** 
> Resource modeling(수정 예정)
> 
> 1️⃣ 회원 관련 API
> 
>   |  HTTP |  Path |  Method |  Permission |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**POST** |/account/signup/|CREATE| AllowAny |사용자 회원가입|
>   |**POST** |/account/login/|NONE| AllowAny |사용자 로그인, access_token, refresh_token 생성 및 반환|
>   |**POST** |/account/logout/|NONE| IsAuthenticated |사용자 로그아웃, BlacklistedToken에 refresh_token 추가|
> 
> 
> 2️⃣ 루틴 관련 API
> 
>   |  HTTP |  Path |  Method |  Permission |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET**, **POST** |/routines/|LIST, CREATE| IsAuthenticated and Access_token |자신의 이번주 루틴 조회 및 생성|
>   |**GET** |/routines/?q={%Y-%m-%d}|LIST| IsAuthenticated and Access_token |쿼리 스트링에 맞는 자신의 해당 요일 루틴 조회|
>   |**GET**, **PUT**, **DELETE** |/routines/<int:pk>/|RETRIEVE, UPDATE, DESTORY| IsAuthenticated and Access_token |자신의 루틴 단건 확인, 수정, 삭제|
>   |**GET** |/routines/<int:pk>/result/|LIST| IsAuthenticated and Access_token |pk에 해당하는 routine_id를 가진 결과 조회|
>   |**PUT**, **DELETE** |/routines/<int:id>/result/<int:pk>/|UPDATE, DESTORY| IsAuthenticated and Access_token |id에 해당하는 routine_id를 가진 루틴의 해당 pk를 가진 결과 수정, 삭제|

<br>

### ***ERD*** 🏳

> ![image](https://user-images.githubusercontent.com/95459089/220845429-e796fc1c-5079-436b-b1e2-cc3199f01723.png)

<br>

### ***process*** 🚀
>
> #### 회원관련 API
> ##### 사용자 회원가입
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220850047-98b40df0-19f0-4516-9c98-33955e39ef6f.png)
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220853603-1e21b77d-37cc-4361-88e9-c3515797db5e.png)
> 
> ##### 사용자 로그인
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220854196-9ab534b6-7cb8-47fd-a6c5-4577ecbaa2b7.png)
> - 응답
> 
> ![image](https://user-images.githubusercontent.com/95459089/220854313-257119af-faa7-4b9e-84db-8f8cc74edfda.png)
> ##### 로그아웃
>
> - access_token 세팅
>
> ![image](https://user-images.githubusercontent.com/95459089/220854533-dfb0b38d-940a-40e6-8276-b779fc4c01b8.png)
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220854698-3c2efdb8-20bd-4a13-a6c2-deb19897822a.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220854766-253c134e-4e26-4562-b5b1-ba63b39f94e0.png)
>
> #### 루틴 관련 API
> - access_token 세팅
> 
> ![image](https://user-images.githubusercontent.com/95459089/220854533-dfb0b38d-940a-40e6-8276-b779fc4c01b8.png)
> 
> ##### 루틴 생성
> 
> - 요청 
>
> ![image](https://user-images.githubusercontent.com/95459089/220855636-fd19a3c7-9ceb-4eee-af36-01d7ca2adcc7.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220855717-203ef8d0-c6a4-4782-aaf4-f64b89d4f174.png)
>
> ##### 이번주 루틴 조회
>
> - 요청
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856237-db187a4e-e5eb-4a91-86c3-c850c607654a.png)
>  
> - 응답
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856027-49fe2215-dc95-4dbd-8683-73b1aa7d2468.png)
>
> ##### 루틴 요일 조회
>
> - 요청
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856180-82d6824a-24ee-4583-ba98-a34f8ec6bba4.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220856349-94b4167d-30af-4011-ad7f-3bfc6dc8cf40.png)
>
> ##### 루틴 수정
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220856590-e3789983-ebf3-4404-be77-df65e14faefe.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220856651-b9d7dd9d-5450-4ec9-9305-2fa839f77fa3.png)
>
> ##### 루틴 단건 조회
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220856815-62f2e835-bd6e-45bd-aa62-49bbaffab589.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220856877-b2139b78-ed44-49ea-b4f3-90ce39113a8e.png)
>
> ##### 루틴 단건 삭제
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220857062-2157696b-5740-465f-971c-c4c389045ea2.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220857113-086a5df8-36a8-4937-8071-2352b30c9d0a.png)
>
> ##### 루틴 결과 조회
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220857492-5e4cd0cf-ecf9-4bc8-b461-3a92fc37e5f8.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220857525-7b4a50f1-fd6e-433d-b4d3-f132db20be9e.png)
>
> ##### 루틴 결과 삭제
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220857752-5d957cc5-6802-42a4-a6a0-aafb350fa9c0.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220857803-bd6d5ba6-1673-4e5f-a668-1c8a7d231cc9.png)
>
> ##### 루틴 결과 수정
>
> - 요청
>
> ![image](https://user-images.githubusercontent.com/95459089/220857961-e804ccb8-8a03-40b3-9bbe-35a48e064e3b.png)
>
> - 응답
>
> ![image](https://user-images.githubusercontent.com/95459089/220858026-0772b0c8-929b-4894-957d-f9674015f762.png)

### Installation

**Backend**
>
> <br>
> 
> **1. Baenaon repository clone**
> 
> ```bash
> git clone https://github.com/donghyeok1/danbi_problem.git
> ```
> **2. backend 환경 설정**
>
> ```bash
> cd danbi_problem
> ```
> **2-1 가상환경 생성 및 실행(git bash)**
>
> ```bash
> python -m venv myvenv
> source myvenv/Scripts/activate
> ```
>
> **2-2 requirements 라이브러리 설치**
> 
> ```bash
> pip install -r requirements.txt
> ```
>
> **3. MySQL 데이터베이 생성 후 장고와 연동**
> 
> - MySQL Workbench 접속 후 새로운 connection 생성
> 
> ![image](https://user-images.githubusercontent.com/95459089/220859628-94c82e21-dedc-48e5-964d-10f4c6019b94.png)
> 
> - 생성 후, 접속해서 데이터 베이스 생성
> 
> ```sql
> CREATE DATABASE danbi;
> ```
>
> - 왼쪽 스키마에 danbi 데이터 베이스 생긴 것 확인
>
> ![image](https://user-images.githubusercontent.com/95459089/220860128-5dcb7197-24d7-41d7-8156-073dbfb30264.png)
>
> - VSC나 Pycharm을 이용해 danbi_problem 프로젝트 열기
> - danbi_problem app의 settings.py에 데이터베이스 설정
> ```python
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.mysql',
>         'NAME': 'danbi',
>         'USER': 'root',
>         'PASSWORD': '[root 계정의 비밀번호]',
>         'HOST': '127.0.0.1',
>         'PORT': '3306',
>         'OPTIONS': {
>             'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
>         }
>     }
> }
> ```
> 
> - bash에서 migrate 진행 (생성한 myvenv 가상환경이 activate 되어 있는 상태여야 함.)
>
> ```bash
> python manage.py makemigrations
> python manage.py migrate
> ```
> 
> - 그 후, MySQL Workbench를 보면 아래 그림처럼 테이블들이 생긴 것을 볼 수 있다.
> 
> ![image](https://user-images.githubusercontent.com/95459089/220861158-1776f24d-b8aa-43d6-9e88-4937460a129b.png)
\
>
> **4. 서버 실행**
> ```bash
> python manage.py runserver
> ```
> 
