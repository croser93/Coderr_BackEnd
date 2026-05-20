from rest_framework.test import APITestCase, APIClient
from django.urls import reverse 
from rest_framework import status

class RegistrationTest(APITestCase):

    def test_registration(self):
        url = reverse('registration')
        data = {
            "username": "andrey Hermann",
            "email": "andrey@gmx.de",
            "password": "asdasd",
            "repeated_password": "asdasd",
            "type": "customer"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        

class BadRegistrationTest(APITestCase):

    def test_bad_registration_400(self):
        url = reverse('registration')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
