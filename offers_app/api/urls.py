from django.urls import path
from .views import OfferListView



urlpatterns = [
    path('offers/', OfferListView.as_view() ,name='profile'),
    # path('offers/<int:pk>/', .as_view(), name='profile_detail'),
    # path('offersdetails/<int:pk>/', .as_view(), name='profile_detail'),

]