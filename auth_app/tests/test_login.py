from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@test.de', password='123456', username='testuser')

    def test_login(self):
        url = reverse('login')
        data = {
            'email':'testuser@test.de',
            'password':'123456'
        }

        response = self.client.post(url, data)
        self.assertIsInstance(response.data['token'], str)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertIsInstance(response.data['user_id'], int)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Unhappy Path
    def test_bad_login_400(self):
        url = reverse('login')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
