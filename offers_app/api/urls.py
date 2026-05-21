from django.urls import path
from .views import OfferListView, OfferDetailView, OfferDetailsIdView



urlpatterns = [
    path('offers/', OfferListView.as_view() ,name='offers'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offers_detail'),
    path('offersdetails/<int:pk>/', OfferDetailsIdView.as_view(), name='offers_detail')

]