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


        self.offer = OfferModel.objects.create(title='test', description='dies ist eine test beschreibung', user=self.business_user,)
        self.detail = DetailModel.objects.create(offer=self.offer, title='test', revisions= 2 ,delivery_time_in_days= 5, price=300, features=['superduper',"test"], offer_type='basic' )
        
        self.userprofile_costumer = UserProfile.objects.create(user=self.user, type='customer')
        self.userprofile_business = UserProfile.objects.create(user=self.business_user, type='business')

        self.token = Token.objects.create(user=self.user)
        self.token_business = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


# test /api/offers/
    def test_get_offers(self):
        url = reverse('offers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_post_offers(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data, [])


# test /api/offers/{id}/
    def test_get_offer_id(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])
        self.assertIsInstance(response.data, dict)

    def test_patch_offer_id(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            "title": "Neues Design für User",
        }
        response = self.client.patch(url, data=new_data, format='json')

        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['title'], new_data['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_offer_id(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# test /api/offerdetails/{id}/
    def test_get_offerdetails_id(self):
        url = reverse('offers_details_id', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#Unhappy Path check Error Code 400, 401, 403, 404 ###############################################################


# Unhappy test /api/offers/
    def test_post_offer_400(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = copy.deepcopy(self.data)
        new_data['details'].pop(1)
        response = self.client.post(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_401(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_403(self):
        url = reverse('offers')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Unhappy test /api/offers/{id}/
    def test_get_offer_id_401(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_id_404(self):
        url = reverse('offers_detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_offer_id_400(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            "title": True,
        }
        response = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_offer_id_401(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        new_data = {
            "title": "Ein test für Fehler 401",
        }
        response = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_patch_offer_id_403(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_data = {
            "title": "Ein test für Fehler 403",
        }
        response = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_id_404(self):
        url = reverse('offers_detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        new_data = {
            "title": "Ein test für Fehler 404",
        }
        response = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer_id_401(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_offer_id_403(self):
        url = reverse('offers_detail', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_id_404(self):
        url = reverse('offers_detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Unhappy test /api/offerdetails/{id}/
    def test_get_offerdetails_id_401(self):
        url = reverse('offers_details_id', kwargs={'pk': self.offer.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offerdetails_id_404(self):
        url = reverse('offers_details_id', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_business.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)