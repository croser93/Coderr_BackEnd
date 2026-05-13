from django.urls import path
from .views import OfferListView, OfferDetailView



urlpatterns = [
    path('offers/', OfferListView.as_view() ,name='profile'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='profile_detail'),
    # path('offersdetails/<int:pk>/', .as_view(), name='profile_detail'),

]