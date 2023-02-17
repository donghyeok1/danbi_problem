from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UserRegistrationAPIViewTestCase(APITestCase):
    def test_registration(self):
        url = reverse("user_signup")
        user_data = {
            "email" : "07385@naver.com",
            "password" : "password!12"
            #"password": "password12"
        }

        response = self.client.post(url, user_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)