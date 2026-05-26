from rest_framework.test import APITestCase, APIClient
from django.urls import reverse 
from rest_framework import status

class RegistrationTest(APITestCase):

    def test_registration(self):
        url = reverse('registration')
        data = {
            "username": "andrey",
            "email": "andrey@gmx.de",
            "password": "asdasd",
            "repeated_password": "asdasd",
            "type": "customer"
        }
        response = self.client.post(url, data)
        self.assertIsInstance(response.data['user_id'], int)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertIsInstance(response.data['token'], str)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class BadRegistrationTest(APITestCase):
# Unhappy Path
    def test_bad_registration_400(self):
        url = reverse('registration')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
