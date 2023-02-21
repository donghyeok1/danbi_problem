from django.test import TestCase

import rest_framework_simplejwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoutineAPITest(APITestCase):
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

        self.create_read_routine_url = reverse('routine-list')
        #self.update_delete_detail_routine_url = reverse('routine-detail')
        # self.read_routine_result_url = reverse('routine-result-list')
        # self.update_delete_routine_url = reverse('routine-result-detail')

        token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(token)
        self.access_token = str(token.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)



    def test_create_routine_success(self):
        """ 루틴 생성 성공 """

        # 주어줘야할 데이터 생성
        data = {
            "title" : "유효성 테스트",
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        # 기본적인 상태 검사
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual({
            'msg': 'You have successfully created the routine.',
            'status': 'ROUTINE_CREATE_OK'
        }, response.json()['message'])


    def test_create_routine_fail_no_title(self):
        """ 루틴 생성 실패 """

        data = {
            "title": "",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_category(self):
        """ 루틴 생성 실패 """

        data = {
            "title": "title",
            "category": "",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_goal(self):
        """ 루틴 생성 실패 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_goal(self):
        """ 루틴 생성 실패 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def tearDown(self):
        self.User.objects.all().delete()

