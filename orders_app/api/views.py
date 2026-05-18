from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from orders_app.models import OrdersModel
from .serializers import OrdersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User



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
        
    def patch(self, request, pk):
        try:
            order = OrdersModel.objects.get(pk=pk)
            serializer = OrdersSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data, status=200)
            return Response ({"error" : "Ungültige Anfragedaten oder unvollständige Details."}, status=400)
        except OrdersModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
        
    def delete(self, request, pk):
        try:
            order = OrdersModel.objects.get(pk=pk)
            order.delete()
            return Response (status=204)
        except OrdersModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
        
class BusinessUserCountView(APIView):
    
    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
            if user.profile.type == 'business':
                order_count = OrdersModel.objects.filter(business_user_id = business_user_id, status='in_progress').count()
                return Response({ "order_count": order_count})
            else:
                return Response ({"error" : "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        except User.DoesNotExist:
            return Response ({"error" : "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        
class BusinessUserCountCompletedView(APIView):
    
    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
            if user.profile.type == 'business':
                order_count = OrdersModel.objects.filter(business_user_id = business_user_id, status='completed').count()
                return Response({ "completed_order_count": order_count})
            else:
                return Response ({"error" : "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        except User.DoesNotExist:
            return Response ({"error" : "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
