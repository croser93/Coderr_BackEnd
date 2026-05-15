
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OfferPostSerializer, OfferGetSerializer, OfferDetailSerializer, OfferDetailsIdSerializer
from offers_app.models import OfferModel, DetailModel
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUserOrAdmin
from .pagination import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class OfferListView(generics.ListCreateAPIView):

    queryset = OfferModel.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUserOrAdmin]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['creator_id', 'min_price', 'max_delivery_time']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price' ]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferPostSerializer
        return OfferGetSerializer
  
        
class OfferDetailView(APIView):

    permission_classes = [IsAuthenticated, IsBusinessUserOrAdmin]

    def get(self, request, pk):
        try:
            offer = OfferModel.objects.get(pk=pk)
            serializer = OfferDetailSerializer(offer)
            return Response (serializer.data)
        except OfferModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
    
    def patch(self, request, pk):
        try:
            offer = OfferModel.objects.get(pk=pk)
            self.check_object_permissions(request, offer)
            serializer = OfferDetailSerializer(offer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data, status=200)
            return Response ({"error" : "Ungültige Anfragedaten oder unvollständige Details."}, status=400)
        except OfferModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
        
    def delete(self, request, pk):
        try:
            offer = OfferModel.objects.get(pk=pk)
            self.check_object_permissions(request, offer)
            offer.delete()
            return Response (status=204)
        except OfferModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
           
class OfferDetailsIdView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            offer_detail = DetailModel.objects.get(pk=pk)
            serializer = OfferDetailsIdSerializer(offer_detail)
            return Response(serializer.data, status=200)
        except DetailModel.DoesNotExist:
            return Response ({"error" : "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)



