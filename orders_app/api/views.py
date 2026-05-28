from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from orders_app.models import OrdersModel
from .serializers import OrdersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from .permissions import IsBusinessUserOrAdmin
from offers_app.models import DetailModel


class OrderListView(APIView):
    """
    View list for orders.

    Endpoints:
    - GET /api/orders/ - Get a list of orders.
    - Post /api/orders/ - Post a single of order.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = OrdersSerializer(data=request.data)
            self.check_object_permissions(request, request)
            if serializer.is_valid():
                serializer.save(customer_user=self.request.user)
                return Response(serializer.data, status=201)
            else:
                return Response({"error": "Ungültige Anfragedaten."}, status=400)
        except DetailModel.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def get(self, request):
        order = OrdersModel.objects.filter(
            Q(customer_user=request.user) | Q(business_user=request.user))
        serializer = OrdersSerializer(order, many=True)
        return Response(serializer.data, status=200)


class OrderDetailView(APIView):
    """
    View for single order.

    Endpoints:
    - GET /api/orders/{id}/ - Get single of offer.
    - PATCH /api/orders/{id}/ - Patch a single offer.
    - DELETE /api/orders/{id}/ - Delete a single offer
    """

    permission_classes = [IsAuthenticated, IsBusinessUserOrAdmin]

    def get(self, request, pk):
        try:
            order = OrdersModel.objects.get(pk=pk)
            serializer = OrdersSerializer(order)
            return Response(serializer.data)
        except OrdersModel.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def patch(self, request, pk):
        try:
            order = OrdersModel.objects.get(pk=pk)
            self.check_object_permissions(request, order)
            serializer = OrdersSerializer(
                order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"error": "Ungültige Anfragedaten oder unvollständige Details."}, status=400)
        except OrdersModel.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def delete(self, request, pk):
        try:
            order = OrdersModel.objects.get(pk=pk)
            self.check_object_permissions(request, order)
            order.delete()
            return Response(status=204)
        except OrdersModel.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)


class BusinessUserCountView(APIView):
    """
    View for order count.
    
    Endpoints:
    - GET /api/order-count/{business_user_id}/- Get a order_count of Business User.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
            if user.profile.type == 'business':
                order_count = OrdersModel.objects.filter(
                    business_user_id=business_user_id, status='in_progress').count()
                return Response({"order_count": order_count})
            else:
                return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        except User.DoesNotExist:
            return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)


class BusinessUserCountCompletedView(APIView):
    """
    View for complete order count.
    
    Endpoints:
    - GET /api/completed-order-count/{business_user_id}/- Get a completed_order_count of Business User.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
            if user.profile.type == 'business':
                order_count = OrdersModel.objects.filter(
                    business_user_id=business_user_id, status='completed').count()
                return Response({"completed_order_count": order_count})
            else:
                return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
        except User.DoesNotExist:
            return Response({"error": "Kein Geschäftsnutzer mit der angegebenen ID gefunden."}, status=404)
