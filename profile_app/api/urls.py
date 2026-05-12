from django.urls import path
from .views import ProfileListView


urlpatterns = [
    path('profile/', ProfileListView.as_view() ,name='profile'),
    path('profile/<int:pk>',name='profile_detail'),
    path('profile/business',name='business_profile'),
    path('profile/customer',name='customer_profile'),


]