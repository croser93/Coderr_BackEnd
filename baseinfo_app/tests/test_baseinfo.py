from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from offers_app.models import OfferModel, DetailModel
from reviews_app.models import ReviewModel
from auth_app.models import UserProfile



class BaseinfoTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.business_user = User.objects.create_user(username='business_user', password='123456', email='business@test.de')

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.offer = OfferModel.objects.create(title='test', description='dies ist eine test beschreibung', user=self.user,)
        self.detail = DetailModel.objects.create(offer=self.offer, title='test', revisions= 2 ,delivery_time_in_days= 5, price=300, features=['superduper',"test"], offer_type='basic' )
        self.review = ReviewModel.objects.create(business_user=self.business_user, reviewer=self.user, rating=5, description='geil gemacht')
        self.userprofile_costumer = UserProfile.objects.create(user=self.user, type='customer')
        self.userprofile_business = UserProfile.objects.create(user=self.business_user, type='business')


    def test_get_baseinfo(self):
        url = reverse('base_info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 5.0)
        self.assertEqual(response.data['review_count'], 1)
        self.assertEqual(response.data['business_profile_count'], 1)
        self.assertEqual(response.data['offer_count'], 1)