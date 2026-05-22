from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import copy

from offers_app.models import OfferModel, DetailModel
from reviews_app.models import ReviewModel
from auth_app.models import UserProfile


class OffersTest(APITestCase):

    data = {
        "title": "Grafikdesign-Paket",
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
    }

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456', email='test@test.de')
        self.business_user = User.objects.create_user(username='business_user', password='123456', email='business@test.de')


        self.offer = OfferModel.objects.create(title='test', description='dies ist eine test beschreibung', user=self.user,)
        self.detail = DetailModel.objects.create(offer=self.offer, title='test', revisions= 2 ,delivery_time_in_days= 5, price=300, features=['superduper',"test"], offer_type='basic' )
        
        self.userprofile_costumer = UserProfile.objects.create(user=self.user, type='customer')
        self.userprofile_business = UserProfile.objects.create(user=self.business_user, type='business')

        self.token = Token.objects.create(user=self.user)
        self.token_business = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_offers(self):
        url = reverse('offers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_post(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data, [])


    #Bad Request Path
    def test_get_post_400(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = copy.deepcopy(self.data)
        new_data['details'].pop(1)
        response = self.client.post(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_post_401(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_post_403(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

