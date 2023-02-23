from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from routine.models import Routine, RoutineResult
from rest_framework.test import APIClient


class RoutineCreateAPITest(APITestCase):
    User = get_user_model()
    """
    Routine CRUD 중 Create 테스트
    """
    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 생성 url, 유저 토큰 인증 설정 """
        self.email = "test@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )
        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def tearDown(self):
        """ 루틴 생성 초기 설정 데이터 초기화 """
        self.client = None
        self.email = None
        self.password = None
        self.user = None

        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.create_routine_url = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_create_routine_success(self):
        """ 루틴 생성 성공 및 루틴 결과 default 생성 성공 """

        data_category_homework = {
            "title" : "유효성 테스트",
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        data_category_miracle = {
            "title": "유효성 테스트",
            "category": "MIRACLE",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response_hw = self.client.post(self.create_routine_url, data=data_category_homework, format='json')
        routine_id = response_hw.data['data']['routine_id']
        routine_hw_result = RoutineResult.objects.get(routine_id=routine_id)

        self.assertEqual(response_hw.status_code, status.HTTP_201_CREATED)
        self.assertEqual({
            'msg': 'You have successfully created the routine.',
            'status': 'ROUTINE_CREATE_OK'
        }, response_hw.json()['message'])
        self.assertIsNotNone(routine_hw_result)

        response_mc = self.client.post(self.create_routine_url, data=data_category_miracle, format='json')
        routine_id = response_mc.data['data']['routine_id']
        routine_mc_result = RoutineResult.objects.get(routine_id=routine_id)

        self.assertEqual(response_mc.status_code, status.HTTP_201_CREATED)
        self.assertEqual({
            'msg': 'You have successfully created the routine.',
            'status': 'ROUTINE_CREATE_OK'
        }, response_mc.json()['message'])
        self.assertIsNotNone(routine_mc_result)



    def test_create_routine_fail_no_title(self):
        """ 루틴 생성 실패 : title 공란 """

        data = {
            "title": "",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_category(self):
        """ 루틴 생성 실패 : category 공란 """

        data = {
            "title": "title",
            "category": "",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_not_validate_category(self):
        """ 루틴 생성 실패 : category의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "숙제",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_goal(self):
        """ 루틴 생성 실패 : goal 공란 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_not_validate_is_alarm(self):
        """ 루틴 생성 실패 : category의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "숙제",
            "goal": "Increase your problem-solving skills",
            "is_alarm": '네',
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_day(self):
        """ 루틴 생성 실패 : days 공란 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": []
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_not_validate_day(self):
        """ 루틴 생성 실패 : days의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["월요일"]
        }

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_routine_fail_no_authorization(self):
        """ 루틴 생성 실패 : 인증 받지 못한 유저 """

        data = {
            "title": "유효성 테스트",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token + "no")

        response = self.client.post(self.create_routine_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoutineUpdateAPITest(APITestCase):
    User = get_user_model()
    """
    Routine CRUD 중 Update 테스트
    """
    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 수정 url, 유저 토큰 인증 설정 """
        self.user1_email = "test1@naver.com"
        self.user1_password = "test123!"
        self.user1 = self.User.objects.create(
            email=self.user1_email,
            password=make_password(self.user1_password)
        )
        self.user2_email = "test2@naver.com"
        self.user2_password = "test123!"
        self.user2 = self.User.objects.create(
            email=self.user2_email,
            password=make_password(self.user2_password)
        )

        self.create_routine_url = reverse('routine-list')

        self.user1_token = TokenObtainPairSerializer.get_token(self.user1)
        self.user1_refresh_token = str(self.user1_token)
        self.user1_access_token = str(self.user1_token.access_token)

        self.user2_token = TokenObtainPairSerializer.get_token(self.user2)
        self.user2_refresh_token = str(self.user2_token)
        self.user2_access_token = str(self.user2_token.access_token)

        self.client1 = APIClient()
        self.client2 = APIClient()

        self.client1.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user1_access_token)
        self.client2.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user2_access_token)

        user1_routine = {
            "title": "user1의 루틴",
            "category": "HOMEWORK",
            "goal": "user1 루틴 테스트 코드 통과하기!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        user2_routine = {
            "title": "user2의 루틴",
            "category": "MIRACLE",
            "goal": "user1 루틴 테스트 코드 통과하기!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response_user1 = self.client1.post(self.create_routine_url, data=user1_routine, format='json')
        self.user1_routine_id = response_user1.data['data']['routine_id']

        response_user2 = self.client2.post(self.create_routine_url, data=user2_routine, format='json')
        self.user2_routine_id = response_user2.data['data']['routine_id']

        self.user1_update_url = self.create_routine_url + str(self.user1_routine_id) + '/'
        self.user2_update_url = self.create_routine_url + str(self.user2_routine_id) + '/'

    def tearDown(self):
        """ 루틴 수정 초기 설정 데이터 초기화 """
        self.client1 = None
        self.client2 = None
        self.create_routine_url = None
        self.user1_update_url = None
        self.user2_update_url = None

        self.user1_routine_id = None
        self.user2_routine_id = None

        self.user1 = None
        self.user1_email = None
        self.user1_password = None
        self.user1_token = None
        self.user1_refresh_token = None
        self.user1_access_token = None

        self.user2 = None
        self.user2_email = None
        self.user2_password = None
        self.user2_token = None
        self.user2_refresh_token = None
        self.user2_access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_update_routine_success(self):
        """ 루틴 수정 성공 : 유저 2명 """

        user1_update_data = {
            "title" : "user1의 수정 루틴",
            "category" : "HOMEWORK",
            "goal": "user1의 수정 테스트 통과",
            "is_alarm": False,
            "days": ["MON", "FRI"]
        }

        user2_update_data = {
            "title": "user2의 수정 루틴",
            "category": "MIRACLE",
            "goal": "user2의 수정 테스트 통과",
            "is_alarm": True,
            "days": ["WED", "FRI"]
        }

        user1_response = self.client1.put(self.user1_update_url, data=user1_update_data, format='json')

        self.assertEqual(user1_response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "msg": "The routine has been modified.",
            "status": "ROUTINE_UPDATE_OK"
        }, user1_response.json()['message'])

        user2_response = self.client2.put(self.user2_update_url, data=user2_update_data, format='json')

        self.assertEqual(user2_response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "msg": "The routine has been modified.",
            "status": "ROUTINE_UPDATE_OK"
        }, user2_response.json()['message'])



    def test_update_routine_fail_no_title(self):
        """ 루틴 수정 실패 : title 공란 """

        data = {
            "title": "",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_no_category(self):
        """ 루틴 수정 실패 : category 공란 """

        data = {
            "title": "title",
            "category": "",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_not_validate_category(self):
        """ 루틴 수정 실패 : category의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "숙제",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_no_goal(self):
        """ 루틴 수정 실패 : goal 공란 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_not_validate_is_alarm(self):
        """ 루틴 생성 실패 : category의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "숙제",
            "goal": "Increase your problem-solving skills",
            "is_alarm": '네',
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_no_day(self):
        """ 루틴 수정 실패 : days 공란 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": []
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_not_validate_day(self):
        """ 루틴 수정 실패 : days의 올바르지 않은 데이터 형식 """

        data = {
            "title": "title",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["월요일"]
        }

        response = self.client1.put(self.user1_update_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_fail_no_authorization(self):
        """ 루틴 수정 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴일 경우 """

        data = {
            "title": "유효성 테스트",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        self.client1.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user1_access_token + "no")

        response = self.client1.put(self.user1_update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_update_routine_fail_forbidden_or_not_found(self):
        """ 루틴 수정 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴일 경우 """

        data = {
            "title": "유효성 테스트",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client2.put(self.user1_update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class RoutineREADAPITest(APITestCase):
    User = get_user_model()
    """
    Routine CRUD 중 Read 테스트
    """

    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 리스트 url, 유저 토큰 인증 설정 """
        self.email = "test1@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        user_routine1 = {
            "title": "user의 루틴1",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기1!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=user_routine1, format='json')
        self.first_routine_id = response.data['data']['routine_id']

        self.user_read_first_url = self.create_routine_url + str(self.first_routine_id) + '/'

        user_routine2 = {
            "title": "user의 루틴2",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기2!",
            "is_alarm": True,
            "days": ["TUE", "THU", "SAT", "SUN"]
        }

        response = self.client.post(self.create_routine_url, data=user_routine2, format='json')
        self.second_routine_id = response.data['data']['routine_id']

        self.user_read_second_url = self.create_routine_url + str(self.second_routine_id) + '/'


    def tearDown(self):
        """ 루틴 읽기 초기 설정 데이터 초기화 """
        self.client = None

        self.create_routine_url = None
        self.user_read_first_url = None
        self.user_read_second_url = None

        self.first_routine_id = None
        self.second_routine_id = None

        self.user = None
        self.email = None
        self.password = None
        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_read_single_routine_success(self):
        """ 루틴 단건 읽기 성공 """

        response_first = self.client.get(self.user_read_first_url, format='json')

        self.assertEqual(response_first.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_DETAIL_OK"
        }, response_first.json()['message'])
        self.assertEqual("user의 루틴1", response_first.json()['data']['title'])

        response_second = self.client.get(self.user_read_second_url, format='json')

        self.assertEqual(response_second.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_DETAIL_OK"
        }, response_second.json()['message'])
        self.assertEqual("user의 루틴2", response_second.json()['data']['title'])


    def test_read_single_routine_success(self):
        """ 이번 주 루틴 읽기 성공 """

        response = self.client.get(self.create_routine_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
        self.assertEqual({
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_LIST_OK"
        }, response.json()['message'])

    def test_read_specific_routine_success(self):
        """ 특정 요일 루틴 읽기 성공 """

        def get_date():
            dt_now = datetime.now()
            return dt_now.strftime('%Y-%m-%d')

        today = get_date()
        today_routine_url = self.create_routine_url + "?q=" + today

        response = self.client.get(today_routine_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 1)
        self.assertEqual({
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_LIST_OK"
        }, response.json()['message'])

    def test_read_single_routine_fail_no_authorization(self):
        """ 루틴 단건 읽기 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴 """

        """ 존재하지 않는 루틴 """
        response = self.client.get(self.create_routine_url + "1000/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """ 자신의 루틴이 아님 """
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token + "32")
        response = self.client.get(self.user_read_first_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoutineDELETEAPITest(APITestCase):
    User = get_user_model()
    """
    Routine CRUD 중 delete 테스트
    """

    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 리스트 url, 유저 토큰 인증 설정 """
        self.email = "test1@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        routine = {
            "title": "user의 루틴1",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기1!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=routine, format='json')
        self.routine_id = response.data['data']['routine_id']

        self.delete_routine_url = self.create_routine_url + str(self.routine_id) + '/'


    def tearDown(self):
        """ 루틴 읽기 초기 설정 데이터 초기화 """
        self.client = None

        self.create_routine_url = None
        self.delete_routine_url = None

        self.routine_id = None

        self.user = None
        self.email = None
        self.password = None
        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_delete_routine_success(self):
        """ 루틴 삭제 성공 """

        response = self.client.delete(self.delete_routine_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual({
            "msg": "The routine has been deleted.",
            "status": "ROUTINE_DELETE_OK"
        }, response.data['message'])
        self.assertEqual(self.routine_id, response.data['data']['routine_id'])

    def test_delete_routine_fail_no_authorization(self):
        """ 루틴 삭제 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴 """

        """ 존재하지 않는 루틴 """
        response = self.client.delete(self.create_routine_url + "1000/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """ 자신의 루틴이 아님 """
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token + "32")
        response = self.client.delete(self.delete_routine_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoutineResultUPDATEAPITest(APITestCase):
    User = get_user_model()
    """
    Routine Result CRUD 중 update 테스트
    """

    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 리스트 url, 유저 토큰 인증 설정 """
        self.email = "test1@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        routine = {
            "title": "user의 루틴1",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기1!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=routine, format='json')
        self.routine_id = response.data['data']['routine_id']
        routine_result = RoutineResult.objects.get(routine_id=self.routine_id)
        self.routine_result_id = routine_result.routine_result_id

        self.update_routine_result_url = self.create_routine_url + str(self.routine_id) + '/result/' + str(self.routine_result_id) + '/'


    def tearDown(self):
        """ 루틴 읽기 초기 설정 데이터 초기화 """
        self.client = None

        self.create_routine_url = None
        self.update_routine_result_url = None

        self.routine_id = None
        self.routine_result_id = None

        self.user = None
        self.email = None
        self.password = None
        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_update_routine_result_success(self):
        """ 루틴 결과 수정 성공 """

        routine_result = {
            "result" : "DONE"
        }

        response = self.client.put(self.update_routine_result_url, data=routine_result, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            "msg": "The Routine's result has been modified",
            "status": "ROUTINE_RESULT_UPDATE_OK"
        }, response.data['message'])
        self.assertEqual(self.routine_result_id, response.data['data']['routine_result_id'])

    def test_update_routine_result_fail_not_validate_result(self):
        """ 루틴 결과 수정 실패 : 유효하지 않은 result 값 """

        routine_result = {
            "result": "Done"
        }

        response = self.client.put(self.update_routine_result_url, data=routine_result, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_routine_result_fail_no_authorization(self):
        """ 루틴 결과 수정 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴 """

        """ 존재하지 않는 루틴 """
        update_routine_result_wrong_url = self.create_routine_url + str(self.routine_id) + '/result/3/'
        response = self.client.put(update_routine_result_wrong_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """ 자신의 루틴이 아님 """
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token + "32")
        response = self.client.put(self.update_routine_result_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoutineResultREADAPITest(APITestCase):
    User = get_user_model()
    """
    Routine Result CRUD 중 read 테스트
    """

    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 리스트 url, 유저 토큰 인증 설정 """
        self.email = "test1@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        routine = {
            "title": "user의 루틴",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=routine, format='json')
        self.routine_id = response.data['data']['routine_id']
        routine_result = RoutineResult.objects.get(routine_id=self.routine_id)
        self.routine_result_id = routine_result.routine_result_id

        self.read_routine_result_url = self.create_routine_url + str(self.routine_id) + '/result/'


    def tearDown(self):
        """ 루틴 읽기 초기 설정 데이터 초기화 """
        self.client = None

        self.create_routine_url = None
        self.read_routine_result_url = None

        self.routine_id = None
        self.routine_result_id = None

        self.user = None
        self.email = None
        self.password = None
        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_read_routine_result_success(self):
        """ 루틴 결과 조회 성공 """

        response = self.client.get(self.read_routine_result_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['routine_result_id'], self.routine_result_id)

    def test_read_routine_result_fail_no_authorization(self):
        """ 루틴 결과 조회 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴 """

        """ 존재하지 않는 루틴 """
        read_routine_result_wrong_url = self.create_routine_url + '3/results/1/'
        response = self.client.get(read_routine_result_wrong_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """ 자신의 루틴이 아님 """
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token + "32")
        response = self.client.get(self.read_routine_result_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoutineResultDELETEAPITest(APITestCase):
    User = get_user_model()
    """
    Routine Result CRUD 중 delete 테스트
    """

    def setUp(self):
        """ 기본적인 유저 설정 및 루틴 리스트 url, 유저 토큰 인증 설정 """
        self.email = "test1@naver.com"
        self.password = "test123!"
        self.user = self.User.objects.create(
            email=self.email,
            password=make_password(self.password)
        )

        self.create_routine_url = reverse('routine-list')

        self.token = TokenObtainPairSerializer.get_token(self.user)
        self.refresh_token = str(self.token)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        routine = {
            "title": "user의 루틴",
            "category": "HOMEWORK",
            "goal": "user 루틴 테스트 코드 통과하기!",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(self.create_routine_url, data=routine, format='json')
        self.routine_id = response.data['data']['routine_id']
        routine_result = RoutineResult.objects.get(routine_id=self.routine_id)
        self.routine_result_id = routine_result.routine_result_id

        self.delete_routine_result_url = self.create_routine_url + str(self.routine_id) + '/result/' + str(self.routine_result_id) + '/'


    def tearDown(self):
        """ 루틴 읽기 초기 설정 데이터 초기화 """
        self.client = None

        self.create_routine_url = None
        self.delete_routine_result_url = None

        self.routine_id = None
        self.routine_result_id = None

        self.user = None
        self.email = None
        self.password = None
        self.token = None
        self.refresh_token = None
        self.access_token = None

        self.User.objects.all().delete()
        OutstandingToken.objects.all().delete()
        Routine.objects.all().delete()



    def test_delete_routine_result_success(self):
        """ 루틴 결과 삭제 성공 """

        response = self.client.delete(self.delete_routine_result_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['data']['routine_result_id'], self.routine_result_id)
        self.assertEqual({
            "msg": "The routine result has been deleted.",
            "status": "ROUTINE_DELETE_OK"
        }, response.data['message'])

    def test_delete_routine_result_fail_no_authorization(self):
        """ 루틴 결과 조회 실패 : 자신의 루틴이 아니거나 존재하지 않는 루틴 """

        """ 존재하지 않는 루틴 """
        delete_routine_result_wrong_url = self.create_routine_url + '3/results/1/'
        response = self.client.delete(delete_routine_result_wrong_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """ 자신의 루틴이 아님 """
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token + "32")
        response = self.client.delete(self.delete_routine_result_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

