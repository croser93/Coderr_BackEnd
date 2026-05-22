from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from profile_app.models import ProfileModel
from auth_app.models import UserProfile

class ProfileTest(APITestCase):

    patch_data = {  
        "first_name": "Max",
        "last_name": "Mustermann",
        "location": "Berlin",
        "description": "Business description",
        "working_hours": "9-17",
        "email": "max@business.de",
    }

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.user_costumer = User.objects.create_user(username='testuser-Customer', password='123456', email='testc@test.de')

        self.user_profil = UserProfile.objects.create(user=self.user, type='business')
        self.user_profil_customer = UserProfile.objects.create(user=self.user_costumer, type='customer')

        self.profil = ProfileModel.objects.create(user=self.user, file=None, location='Germany', tel='123456789', description='Test User', working_hours='40')
        self.profil_customer = ProfileModel.objects.create(user=self.user_costumer, file=None, location='Germany', tel='123456789', description='Test User', working_hours='40')
        
        
        self.token = Token.objects.create(user=self.user)
        self.token_costumer = Token.objects.create(user=self.user_costumer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
    def test_get_profile(self):
        url = reverse('profile_detail', kwargs={'pk': '1'})
        response = self.client.get(url)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile(self):
        url = reverse('profile_detail', kwargs={'pk': '1'})
        response = self.client.patch(url, self.patch_data)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.data['first_name'], self.patch_data['first_name'])
        self.assertEqual(response.data['last_name'], self.patch_data['last_name'])
        self.assertEqual(response.data['location'], self.patch_data['location'])
        self.assertEqual(response.data['type'], 'business')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profiles_business(self):
        url = reverse('business_profile')
        response = self.client.get(url)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profiles_customer(self):
        url = reverse('customer_profile')
        response = self.client.get(url)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#  Test the Unhappy Path

    def test_get_profile_401(self):
        url = reverse('profile_detail', kwargs={'pk': '1'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_profile_404(self):
        url = reverse('profile_detail', kwargs={'pk': '100'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def test_patch_profile_401(self):
        url = reverse('profile_detail', kwargs={'pk': '1'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.patch(url, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_403(self):
        url = reverse('profile_detail', kwargs={'pk': '1'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_costumer.key)
        response = self.client.patch(url, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_404(self):
        url = reverse('profile_detail', kwargs={'pk': '999'})
        response = self.client.patch(url, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profiles_business_401(self):
        url = reverse('business_profile')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profiles_customer_401(self):
        url = reverse('customer_profile')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertNotEqual(response.data,[])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)