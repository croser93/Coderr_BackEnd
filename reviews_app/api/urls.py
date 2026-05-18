from django.urls import path
from .views import ReviewListView

urlpatterns = [
     path('reviews/', ReviewListView.as_view(), name='reviews'),
    #  path('reviews/<int:pk>/', OrderDetailView.as_view(), name='reviews_detail'),

]
