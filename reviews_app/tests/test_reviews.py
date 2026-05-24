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


class ReviewsTest(APITestCase):
    
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
        self.reviews = ReviewModel.objects.create( business_user=self.business_user, reviewer=self.user, rating=5, description='Super freundlich alles top gelaufen' )
        
        self.userprofile_costumer = UserProfile.objects.create(user=self.user, type='customer')
        self.userprofile_business = UserProfile.objects.create(user=self.business_user, type='business')

        self.token = Token.objects.create(user=self.user)
        self.token_business = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
