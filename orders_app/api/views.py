from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from orders_app.models import OrdersModel
from .serializers import OrdersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class OrderListView(generics.ListCreateAPIView):

    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)


class OrderDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            order = OrdersModel.objects.get(pk=pk)
            serializer = OrdersSerializer(order)
            return Response (serializer.data)
        except OrdersModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)