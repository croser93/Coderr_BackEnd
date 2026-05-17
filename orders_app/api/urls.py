from django.urls import path
from .views import OrderListView, OrderDetailView

urlpatterns = [
     path('orders/', OrderListView.as_view(), name='orders'),
     path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders_detail'),
]
