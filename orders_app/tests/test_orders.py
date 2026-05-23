from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import copy

from offers_app.models import OfferModel, DetailModel
from reviews_app.models import ReviewModel
from auth_app.models import UserProfile
from orders_app.models import OrdersModel


class OrdersTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.business_user = User.objects.create_user(username='business_user', password='123456', email='business@test.de')


        self.offer = OfferModel.objects.create(title='test', description='dies ist eine test beschreibung', user=self.business_user,)
        self.detail = DetailModel.objects.create(offer=self.offer, title='test', revisions= 2 ,delivery_time_in_days= 5, price=300, features=['superduper',"test"], offer_type='basic' )
        self.order = OrdersModel.objects.create(
            customer_user=self.user, 
            business_user=self.business_user,
            title='Test Titel',
            revisions=5,
            delivery_time_in_days=5,
            price=1000,
            features=['style', 'test'],
            offer_type='basic',
            status='in_progress'
            )
        
        self.userprofile_costumer = UserProfile.objects.create(user=self.user, type='customer')
        self.userprofile_business = UserProfile.objects.create(user=self.business_user, type='business')

        self.token = Token.objects.create(user=self.user)
        self.token_business = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        

    def  test_get_order(self):
        url= reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def  test_post_order(self):
        url= reverse('orders')
        data={
              "offer_detail_id": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(len(response.data), 12)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
# Unhappy path


    def  test_get_order_401(self):
        url= reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def  test_post_order_400(self):
        url= reverse('orders')
        data={
              ' '
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def  test_post_order_401(self):
        url= reverse('orders')
        data={
              "offer_detail_id": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def  test_post_order_403(self):
        url= reverse('orders')
        data={
              "offer_detail_id": 1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def  test_post_order_404(self):
        url= reverse('orders')
        data={
              "offer_detail_id": 9999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)