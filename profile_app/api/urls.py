from django.urls import path
from .views import ProfileListView, ProfileDetailView, ProfileCustomerListView, ProfileBusinessListView


urlpatterns = [
    path('profile/', ProfileListView.as_view() ,name='profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/business/', ProfileBusinessListView.as_view(), name='business_profile'),
    path('profile/customer/', ProfileCustomerListView.as_view(), name='customer_profile'),


]