from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from orders_app.models import OrdersModel
from .serializers import OrdersSerializer


class OrderListView(generics.ListCreateAPIView):

    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)
