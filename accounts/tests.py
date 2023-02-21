import rest_framework_simplejwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AccountAPITest(APITestCase):
    User = get_user_model()
    """
    유저 회원가입, 로그인 테스트
    """
    # setUpTestData는 한번만 실행되기 때문에 로그인 테스트를 할 때에는 각 함수들이 실행될 때마다 실행되는 setUp을 씀.
    def setUp(self):
        """ 기본적인 유저 설정 """
        self.email = "test@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.signup_url = reverse('user-signup')
        self.login_url = reverse('user-login')
        self.logout_url = reverse('user-logout')

        token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(token)
        self.access_token = str(token.access_token)


    def test_signup_success(self):
        """ 회원 가입 성공 """

        data = {
            "email" : "test2@naver.com",
            "password" : "test123!"
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_fail_not_email_form(self):
        """ 회원 가입 실패 : 이메일 형식이 아님. """

        data = {
            "email" : "test2",
            "password" : "test!123"
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_length_short_not_include_special(self):
        """ 회원 가입 실패 : 비밀번호 길이가 8자 미만, 특수 문자 포함 x """

        data = {
            "email" : "test3@test.com",
            "password" : "test12"
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_not_include_special(self):
        """ 회원 가입 실패 : 비밀번호가 길이, 숫자는 만족하나, 특수문자 포함 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test123121",
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_legth_short(self):
        """ 회원 가입 실패 : 비밀번호가 특수 문자, 숫자 포함하지만, 길이 만족 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test!12",
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_not_num(self):
        """ 회원 가입 실패 : 비밀번호가 특수 문자 포함, 길이 만족하지만 숫자 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test!@#$",
        }

        response = self.client.post(self.signup_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_login_success(self):
        """ 로그인 성공 """

        login_data = {
            "email" : self.email,
            "password" : self.password,
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.content.decode('utf-8'))
        self.assertTrue('refresh_token' in response.content.decode('utf-8'))

    def test_login_fail_wrong_password(self):
        """ 로그인 실패 : 잘못된 비밀번호 """

        data = {
            "email": self.email,
            "password": self.password + ".",
        }

        response = self.client.post(self.login_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fail_wrong_email(self):
        """ 로그인 실패 : 잘못된 이메일 """

        data = {
            "email" : self.email + ".",
            "password" : self.password,
        }

        response = self.client.post(self.login_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fail_wrong_email_password(self):
        """ 로그인 실패 : 잘못된 이메일 + 잘못된 비밀번호 """

        data = {
            "email" : self.email + ".",
            "password" : self.password + ".",
        }

        response = self.client.post(self.login_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """ 로그아웃 성공 """

        data = {
            "refresh_token" : self.refresh_token
        }
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = client.post(self.logout_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_fail_wrong_refresh_token(self):
        """ 로그아웃 실패 : 엑세스 토큰은 맞는데, 리프레시 토큰 x """

        data = {
            "refresh_token" : self.refresh_token + "d"
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.logout_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_fail_wrong_access_token(self):
        """ 로그아웃 실패 : 리프레시 토큰은 맞는데, 엑세스 토큰 x """

        data = {
            "refresh_token": self.refresh_token
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token + "d")
        response = self.client.post(self.logout_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.User.objects.all().delete()
