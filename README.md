# Danbi ๊ต์ก ๊ณผ์  ๐ฅ

## ***Introduction*** โ

> - ์ํฌ ์๋น์ค ๋ด์ Routine ๊ธฐ๋ฅ์ ์ถ๊ฐํ๊ณ ์ ํฉ๋๋ค.
> - Routine ๊ธฐ๋ฅ์ด๋, ๋งค ์ฃผ๋ง๋ค ์ ํด์ง ์ผ์ ์ ์์ ์ด ํด์ผํ  ์ผ์ ๋ฑ๋กํ๊ณ , ํด๋น ์ํ์ฌ๋ถ์ ๋ํ ๋ด์ฉ์ ๊ธฐ๋กํ์ฌ ๊ด๋ฆฌํ  ์ ์๋๋ก ๋์์ฃผ๋ ๊ธฐ๋ฅ์๋๋ค.
> - Routine ๊ธฐ๋ฅ์์๋ ๋ค์๊ณผ ๊ฐ์ ๊ธฐ๋ฅ์ ์ ๊ณตํ๊ณ ์ ํฉ๋๋ค.
>     - ์ ์ ์ ๋ก๊ทธ์ธ/๋ก๊ทธ์์ ๊ธฐ๋ฅ
>     - ๋งค ์ฃผ๋ณ ํด์ผํ  ์ผ์ ๋ฑ๋ก / ์์  / ์ญ์  / ์กฐํ ๊ธฐ๋ฅ
>     - ์ผ์ ์ด ์ง๋ ํ ์งํํ ํ  ์ผ๋ค์ ๋ํ ํด๊ฒฐ์ฌ๋ถ ๊ธฐ๋ก
>         - ๊ฐ ํ ์ผ์ ๋ํ ๊ฒฐ๊ณผ๋ ๋๋ฆฝ๋ ๊ฒฐ๊ณผ๋ก ๊ธฐ๋ก๋์ด์ผ ํจ
>         - ์์)์/์/๊ธ ํ ์ผ๋ก ๋ฑ๋กํ์ ๋, ํน์  ๋ ์ง ๋ฐ์ดํฐ๋ฅผ ์กฐํํ๋ฉด ์กฐํํ ๋ ์ง์ ๋ํ ์ํ๊ฒฐ๊ณผ๋ง ๋ชจ๋ ์กฐํ๊ฐ ๋๋๋ก ๊ตฌ์ฑ

### ***Summary*** ๐ฝ
> - Project ์๊ฐ
>   - ๋ฃจํด, ๋ฃจํด ๊ฒฐ๊ณผ CRUD ๊ตฌํ
>   - ์นด์นด์ค Map API๋ฅผ ์ด์ฉํ์ฌ ์ง์ญ ๊ฒ์ํ๊ณผ ์ฐ๋
>   - DjangoRestFramework๋ฅผ ์ด์ฉํ์ฌ ํ์, ๋ฃจํด ์ ๋ณด ์ ์ฅ์ฉ REST API ์๋ฒ ๊ตฌํ
>   - JWT๋ฅผ ์ด์ฉํ์ฌ OAuth 2.0 Auth ํ๋กํ ์ฝ ๊ธฐ๋ฐ์ผ๋ก Authentication ๋ฐ Authorization ๊ตฌํ


### ***Requirments*** ๐ค
> - BACKEND(Djagno Authentication Server)
>   - django~=3.0.0
>   - djangorestframework~=3.11.0
>   - djangorestframework-simplejwt
>   - mysqlclient

> - DataBase
>   - MySQL

<br>

### ***IDE*** ๐ฅข
> - BACKEND
>   - Pycharm Professional
>   - VScode
>   - Postman
>   - MySQL Workbench


<br>

### ***Backend End-points*** 
> Resource modeling(์์  ์์ )
> 
> 1๏ธโฃ ํ์ ๊ด๋ จ API
> 
>   |  HTTP |  Path |  Method |  Permission |  ๋ชฉ์  |
>   | --- | --- | --- | --- | --- |
>   |**POST** |/account/signup/|CREATE| AllowAny |์ฌ์ฉ์ ํ์๊ฐ์|
>   |**POST** |/account/login/|NONE| AllowAny |์ฌ์ฉ์ ๋ก๊ทธ์ธ, access_token, refresh_token ์์ฑ ๋ฐ ๋ฐํ|
>   |**POST** |/account/logout/|NONE| IsAuthenticated |์ฌ์ฉ์ ๋ก๊ทธ์์, BlacklistedToken์ refresh_token ์ถ๊ฐ|
> 
> 
> 2๏ธโฃ ๋ฃจํด ๊ด๋ จ API
> 
>   |  HTTP |  Path |  Method |  Permission |  ๋ชฉ์  |
>   | --- | --- | --- | --- | --- |
>   |**GET**, **POST** |/routines/|LIST, CREATE| IsAuthenticated and Access_token |์์ ์ ์ด๋ฒ์ฃผ ๋ฃจํด ์กฐํ ๋ฐ ์์ฑ|
>   |**GET** |/routines/?q={%Y-%m-%d}|LIST| IsAuthenticated and Access_token |์ฟผ๋ฆฌ ์คํธ๋ง์ ๋ง๋ ์์ ์ ํด๋น ์์ผ ๋ฃจํด ์กฐํ|
>   |**GET**, **PUT**, **DELETE** |/routines/<int:pk>/|RETRIEVE, UPDATE, DESTORY| IsAuthenticated and Access_token |์์ ์ ๋ฃจํด ๋จ๊ฑด ํ์ธ, ์์ , ์ญ์ |
>   |**GET** |/routines/<int:pk>/result/|LIST| IsAuthenticated and Access_token |pk์ ํด๋นํ๋ routine_id๋ฅผ ๊ฐ์ง ๊ฒฐ๊ณผ ์กฐํ|
>   |**PUT**, **DELETE** |/routines/<int:id>/result/<int:pk>/|UPDATE, DESTORY| IsAuthenticated and Access_token |id์ ํด๋นํ๋ routine_id๋ฅผ ๊ฐ์ง ๋ฃจํด์ ํด๋น pk๋ฅผ ๊ฐ์ง ๊ฒฐ๊ณผ ์์ , ์ญ์ |

<br>

### ***ERD*** ๐ณ

> ![image](https://user-images.githubusercontent.com/95459089/220845429-e796fc1c-5079-436b-b1e2-cc3199f01723.png)

<br>

### ***process*** ๐
>
> #### ํ์๊ด๋ จ API
> ##### ์ฌ์ฉ์ ํ์๊ฐ์
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220850047-98b40df0-19f0-4516-9c98-33955e39ef6f.png)
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220853603-1e21b77d-37cc-4361-88e9-c3515797db5e.png)
> 
> ##### ์ฌ์ฉ์ ๋ก๊ทธ์ธ
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220854196-9ab534b6-7cb8-47fd-a6c5-4577ecbaa2b7.png)
> - ์๋ต
> 
> ![image](https://user-images.githubusercontent.com/95459089/220854313-257119af-faa7-4b9e-84db-8f8cc74edfda.png)
> ##### ๋ก๊ทธ์์
>
> - access_token ์ธํ
>
> ![image](https://user-images.githubusercontent.com/95459089/220854533-dfb0b38d-940a-40e6-8276-b779fc4c01b8.png)
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220854698-3c2efdb8-20bd-4a13-a6c2-deb19897822a.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220854766-253c134e-4e26-4562-b5b1-ba63b39f94e0.png)
>
> #### ๋ฃจํด ๊ด๋ จ API
> - access_token ์ธํ
> 
> ![image](https://user-images.githubusercontent.com/95459089/220854533-dfb0b38d-940a-40e6-8276-b779fc4c01b8.png)
> 
> ##### ๋ฃจํด ์์ฑ
> 
> - ์์ฒญ 
>
> ![image](https://user-images.githubusercontent.com/95459089/220855636-fd19a3c7-9ceb-4eee-af36-01d7ca2adcc7.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220855717-203ef8d0-c6a4-4782-aaf4-f64b89d4f174.png)
>
> ##### ์ด๋ฒ์ฃผ ๋ฃจํด ์กฐํ
>
> - ์์ฒญ
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856237-db187a4e-e5eb-4a91-86c3-c850c607654a.png)
>  
> - ์๋ต
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856027-49fe2215-dc95-4dbd-8683-73b1aa7d2468.png)
>
> ##### ๋ฃจํด ์์ผ ์กฐํ
>
> - ์์ฒญ
> 
> ![image](https://user-images.githubusercontent.com/95459089/220856180-82d6824a-24ee-4583-ba98-a34f8ec6bba4.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220856349-94b4167d-30af-4011-ad7f-3bfc6dc8cf40.png)
>
> ##### ๋ฃจํด ์์ 
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220856590-e3789983-ebf3-4404-be77-df65e14faefe.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220856651-b9d7dd9d-5450-4ec9-9305-2fa839f77fa3.png)
>
> ##### ๋ฃจํด ๋จ๊ฑด ์กฐํ
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220856815-62f2e835-bd6e-45bd-aa62-49bbaffab589.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220856877-b2139b78-ed44-49ea-b4f3-90ce39113a8e.png)
>
> ##### ๋ฃจํด ๋จ๊ฑด ์ญ์ 
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220857062-2157696b-5740-465f-971c-c4c389045ea2.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220857113-086a5df8-36a8-4937-8071-2352b30c9d0a.png)
>
> ##### ๋ฃจํด ๊ฒฐ๊ณผ ์กฐํ
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220857492-5e4cd0cf-ecf9-4bc8-b461-3a92fc37e5f8.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220857525-7b4a50f1-fd6e-433d-b4d3-f132db20be9e.png)
>
> ##### ๋ฃจํด ๊ฒฐ๊ณผ ์ญ์ 
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/220857752-5d957cc5-6802-42a4-a6a0-aafb350fa9c0.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/220857803-bd6d5ba6-1673-4e5f-a668-1c8a7d231cc9.png)
>
> ##### ๋ฃจํด ๊ฒฐ๊ณผ ์์ 
>
> - ์์ฒญ
>
> ![image](https://user-images.githubusercontent.com/95459089/223625265-ab65ed1b-ce2a-4f8e-8879-a1eb283fd7c9.png)
>
> - ์๋ต
>
> ![image](https://user-images.githubusercontent.com/95459089/223625228-3569ea58-013a-4fbf-a166-3d067f30db1d.png)

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
> **2. backend ํ๊ฒฝ ์ค์ **
>
> ```bash
> cd danbi_problem
> ```
> **2-1 ๊ฐ์ํ๊ฒฝ ์์ฑ ๋ฐ ์คํ(git bash)**
>
> ```bash
> python -m venv myvenv
> source myvenv/Scripts/activate
> ```
>
> **2-2 requirements ๋ผ์ด๋ธ๋ฌ๋ฆฌ ์ค์น**
> 
> ```bash
> pip install -r requirements.txt
> ```
>
> **3. MySQL ๋ฐ์ดํฐ๋ฒ ์ด ์์ฑ ํ ์ฅ๊ณ ์ ์ฐ๋**
> 
> - MySQL Workbench ์ ์ ํ ์๋ก์ด connection ์์ฑ
> 
> ![image](https://user-images.githubusercontent.com/95459089/220859628-94c82e21-dedc-48e5-964d-10f4c6019b94.png)
> 
> - ์์ฑ ํ, ์ ์ํด์ ๋ฐ์ดํฐ ๋ฒ ์ด์ค ์์ฑ
> 
> ```sql
> CREATE DATABASE danbi;
> ```
>
> - ์ผ์ชฝ ์คํค๋ง์ danbi ๋ฐ์ดํฐ ๋ฒ ์ด์ค ์๊ธด ๊ฒ ํ์ธ
>
> ![image](https://user-images.githubusercontent.com/95459089/220860128-5dcb7197-24d7-41d7-8156-073dbfb30264.png)
>
> - VSC๋ Pycharm์ ์ด์ฉํด danbi_problem ํ๋ก์ ํธ ์ด๊ธฐ
> - danbi_problem app์ settings.py์ ๋ฐ์ดํฐ๋ฒ ์ด์ค ์ค์ 
> ```python
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.mysql',
>         'NAME': 'danbi',
>         'USER': 'root',
>         'PASSWORD': '[root ๊ณ์ ์ ๋น๋ฐ๋ฒํธ]',
>         'HOST': '127.0.0.1',
>         'PORT': '3306',
>         'OPTIONS': {
>             'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
>         }
>     }
> }
> ```
> 
> - bash์์ migrate ์งํ (์์ฑํ myvenv ๊ฐ์ํ๊ฒฝ์ด activate ๋์ด ์๋ ์ํ์ฌ์ผ ํจ.)
>
> ```bash
> python manage.py makemigrations
> python manage.py migrate
> ```
> 
> - ๊ทธ ํ, MySQL Workbench๋ฅผ ๋ณด๋ฉด ์๋ ๊ทธ๋ฆผ์ฒ๋ผ ํ์ด๋ธ๋ค์ด ์๊ธด ๊ฒ์ ๋ณผ ์ ์๋ค.
> 
> ![image](https://user-images.githubusercontent.com/95459089/220861158-1776f24d-b8aa-43d6-9e88-4937460a129b.png)
\
>
> **4. ์๋ฒ ์คํ**
> ```bash
> python manage.py runserver
> ```
> 
