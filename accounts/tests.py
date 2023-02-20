from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.utils import aware_utcnow


class AccountAPITest(APITestCase):
    User = get_user_model()
    """
    유저 회원가입, 로그인 테스트
    """
    # setUpTestData는 한번만 실행되기 때문에 로그인 테스트를 할 때에는 각 함수들이 실행될 때마다 실행되는 setUp을 씀.
    def setUp(self):
        """ 기본적인 유저 설정 """
        # self.user_data = {'email': 'test@naver.com', 'password': 'test123!'}
        # self.email = "test@naver.com"
        # self.password = "test123!"
        # self.user = self.User.objects.create(
        #     email=self.email,
        #     password=make_password(self.password)
        # )
        #
        # data = {
        #     "email" : "test@naver.com",
        #     "password" : "test123!"
        # }
        #
        # response = self.client.post(reverse('user-login'), data=data, format='json')
        # decode_res = response.content.decode('utf-8')
        # email, refresh_token, access_token = decode_res.split(",")
        # str_access,  access_tok = access_token.split(":")
        # str_refresh, refresh_tok = refresh_token.split(":")
        # self.access_token = access_tok
        # self.refresh_token = refresh_tok
        # OutstandingToken.objects.create(token=self.refresh_token)
        refresh = RefreshToken()

        # Serializer validates
        ser = TokenRefreshSerializer(data={'refresh': str(refresh)})

        old_jti = refresh['jti']
        old_exp = refresh['exp']

        # Serializer validates
        ser = TokenRefreshSerializer(data={'refresh': str(refresh)})

        now = aware_utcnow() - api_settings.ACCESS_TOKEN_LIFETIME / 2

        with override_api_settings(ROTATE_REFRESH_TOKENS=True, BLACKLIST_AFTER_ROTATION=True):
            with patch('rest_framework_simplejwt.tokens.aware_utcnow') as fake_aware_utcnow:
                fake_aware_utcnow.return_value = now
                self.assertTrue(ser.is_valid())

    access = AccessToken(ser.validated_data['access'])
        new_refresh = RefreshToken(ser.validated_data['refresh'])
        print(access, new_refresh)

    def test_signup_success(self):
        """ 회원 가입 성공 """

        data = {
            "email" : "test2@naver.com",
            "password" : "test123!"
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_not_email_form(self):
        """ 회원 가입 성공 """

        data = {
            "email" : "test2",
            "password" : "test!123"
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_length_short_not_include_special(self):
        """ 회원 가입 실패 : 비밀번호 길이가 8자 미만, 특수 문자 포함 x """

        data = {
            "email" : "test3@test.com",
            "password" : "test12"
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_not_include_special(self):
        """ 회원 가입 실패 : 비밀번호가 길이, 숫자는 만족하나, 특수문자 포함 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test123121",
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_legth_short(self):
        """ 회원 가입 실패 : 비밀번호가 특수 문자, 숫자 포함하지만, 길이 만족 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test!12",
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_not_num(self):
        """ 회원 가입 실패 : 비밀번호가 특수 문자 포함, 길이 만족하지만 숫자 x """

        data = {
            "email" : "test4@test.com",
            "password" : "test!@#$",
        }

        response = self.client.post(reverse('user-signup'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_login_success(self):
        """ 로그인 성공 """

        data = {
            "email" : self.email,
            "password" : self.password,
        }

        response = self.client.post(reverse('user-login'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        """ 로그인 실패 : 잘못된 비밀번호 """

        data = {
            "email": self.email,
            "password": self.password + ".",
        }

        response = self.client.post(reverse('user-login'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_email(self):
        """ 로그인 실패 : 잘못된 이메일 """

        data = {
            "email" : self.email + ".",
            "password" : self.password,
        }

        response = self.client.post(reverse('user-login'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_email_password(self):
        """ 로그인 실패 : 잘못된 이메일 + 잘못된 비밀번호 """

        data = {
            "email" : self.email + ".",
            "password" : self.password + ".",
        }

        response = self.client.post(reverse('user-login'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """ 로그아웃 성공 """

        data = {
            "refresh_token" : self.refresh_token
        }
        print(self.refresh_token, self.access_token)

        response = self.client.post(
            path=reverse('user-logout'),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.User.objects.all().delete()
