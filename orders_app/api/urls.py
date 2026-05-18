from django.urls import path
from .views import OrderListView, OrderDetailView, BusinessUserCountView

urlpatterns = [
     path('orders/', OrderListView.as_view(), name='orders'),
     path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders_detail'),
     path('order-count/<int:business_user_id>/', BusinessUserCountView.as_view(), name='business_user_count'),
]
