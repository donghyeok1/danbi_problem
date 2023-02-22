from django.test import TestCase

import rest_framework_simplejwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from routine.models import Routine, RoutineResult


class RoutineCreateAPITest(APITestCase):
    User = get_user_model()
    """
    CRUD 중 Create 테스트
    """
    def setUp(self):
        """ 기본적인 유저 설정 """
        self.email = "test@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )
        self.create_read_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def tearDown(self):
        self.client = None
        self.email = None
        self.password = None
        self.user = None
        self.create_read_routine_url = None
        self.token = None
        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        BlacklistedToken.objects.all().delete()
        Routine.objects.all().delete()



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

    def test_create_routine_fail_no_day(self):
        """ 루틴 생성 실패 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": []
        }

        response = self.client.post(self.create_read_routine_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

