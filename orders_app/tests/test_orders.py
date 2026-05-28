from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import copy

from offers_app.models import Offers, OffersDetail
from reviews_app.models import Reviews
from auth_app.models import UserProfile
from orders_app.models import Orders


class OrdersTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.business_user = User.objects.create_user(username='business_user', password='123456', email='business@test.de')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123', email='admin@test.com')

        self.offer = Offers.objects.create(title='test', description='dies ist eine test beschreibung', user=self.business_user,)
        self.detail = OffersDetail.objects.create(offer=self.offer, title='test', revisions= 2 ,delivery_time_in_days= 5, price=300, features=['superduper',"test"], offer_type='basic' )
        self.order = Orders.objects.create(
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
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.token = Token.objects.create(user=self.user)
        self.token_business = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
# happy /api/orders/
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

# happy /api/orders/{pk}/    
    def test_patch_order_id(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            'status' : 'completed'
        }
        response= self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_data['status'])

# happy /api/order-count/{business_user_id}/
    def test_get_order_count(self):
        url = reverse('business_user_count', kwargs={'business_user_id': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
 # happy /api/completed-order-count/{business_user_id}/   
    def test_get_complete_orders(self):
        url = reverse('business_user_completed_count', kwargs={'business_user_id': self.business_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
# happy /api/orders/{pk}/         
    def test_delete_order_id(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response= self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
#Unhappy Path check Error Code 400, 401, 403, 404 ###############################################################


# Unhappy test /api/orders/
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
        
# Unhappy test /api/orders/{id}/
    def test_patch_order_id_400(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            'status' : 999
        }
        response= self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    def test_patch_order_id_401(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        new_data = {
            'status' : 'completed'
        }
        response= self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
    def test_patch_order_id_403(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_data = {
            'status' : 'completed'
        }
        response= self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
    def test_patch_order_id_404(self):
        url = reverse('orders_detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            'status' : 'completed'
        }
        response= self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_id_401(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response= self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_order_id_403(self):
        url = reverse('orders_detail', kwargs={'pk': self.order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response= self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_order_id_404(self):
        url = reverse('orders_detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response= self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Unhappy test /api/order-count/{business_user_id}/        
    def test_get_order_count_401(self):
        url = reverse('business_user_count', kwargs={'business_user_id': self.business_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_count_404(self):
        url = reverse('business_user_count', kwargs={'business_user_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Unhappy test /api/completed-order-count/{business_user_id}}/
    def test_get_complete_orders_401(self):
        url = reverse('business_user_completed_count', kwargs={'business_user_id': self.business_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_complete_orders_404(self):
        url = reverse('business_user_completed_count', kwargs={'business_user_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        