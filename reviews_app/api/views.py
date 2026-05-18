from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from .serializers import OrdersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
# from .permissions import IsBusinessUserOrAdmin, IsCustomerUserOrAdmin
from .serializer import ReviewModel
from reviews_app.models import ReviewModel


class ReviewListView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = ReviewModel(data=request.data)
            self.check_object_permissions(request, request)
            if serializer.is_valid():
                serializer.save(customer_user=self.request.user)
                return Response (serializer.data, status=201)  
            else:
              return Response ({"error" : "Ungültige Anfragedaten."}, status=400)  
        except ReviewModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)


    def get(self, request):
        order = ReviewModel.objects.all()
        serializer = ReviewModel(order, many=True)
        return Response (serializer.data, status=200)
