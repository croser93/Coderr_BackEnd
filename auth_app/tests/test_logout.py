from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
class LogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url)

        self.assertFalse(Token.objects.filter(user=self.user).exists())
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    