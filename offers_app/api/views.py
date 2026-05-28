
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OfferPostSerializer, OfferGetSerializer, OfferDetailSerializer, OfferDetailsIdSerializer, OfferDetailPatchSerializer
from offers_app.models import Offers, OffersDetail
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUserOrAdmin
from .pagination import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import OfferFilter
from rest_framework.exceptions import ValidationError

class OfferListView(generics.ListCreateAPIView):
    """
    View List for Offers.  

    Endpoints:
    - GET /api/offers/ - Get list of offers with Query Parameters
    - POST /api/offers/ - Post a new offer  
    Query Parameters = creator_id, min_price, max_delivery_time, ordering and search
    """
    queryset = Offers.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferPostSerializer
        return OfferGetSerializer

    def get_validation_param(self):
        allowed_params = {'creator_id', 'min_price', 'max_delivery_time', 'ordering', 'search', 'page_size', 'page'}
        return set(self.request.query_params.keys()) - allowed_params

    def get_queryset(self):
        if self.get_validation_param():
            raise ValidationError({'error': 'Ungültige Parameter.'})

        queryset = Offers.objects.all()
        ordering = self.request.query_params.get('ordering')
        if ordering == 'min_price':
            queryset = queryset.order_by('details__price')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailView(APIView):
    """
    View for single Offers.
    
    Endpoints:
    - GET /api/offers/{id}/ - Get single of offer.
    - PATCH /api/offers/{id}/ - Patch a single offer.
    - DELETE /api/offers/{id}/ - Delete a single offer
    """
    permission_classes = [IsAuthenticated, IsBusinessUserOrAdmin]

    def get(self, request, pk):
        try:
            offer = Offers.objects.get(pk=pk)
            serializer = OfferDetailSerializer(offer)
            return Response(serializer.data)
        except Offers.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def patch(self, request, pk):
        try:
            offer = Offers.objects.get(pk=pk)
            self.check_object_permissions(request, offer)
            serializer = OfferDetailPatchSerializer(
                offer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"error": "Ungültige Anfragedaten oder unvollständige Details."}, status=400)
        except Offers.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)

    def delete(self, request, pk):
        try:
            offer = Offers.objects.get(pk=pk)
            self.check_object_permissions(request, offer)
            offer.delete()
            return Response(status=204)
        except Offers.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)


class OfferDetailsIdView(APIView):
    """
    View List for Offers.
    
    Endpoints:
    - GET /api/offerdetails/{id}/ - Get a single offer with detail.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            offer_detail = OffersDetail.objects.get(pk=pk)
            serializer = OfferDetailsIdSerializer(offer_detail)
            return Response(serializer.data, status=200)
        except OffersDetail.DoesNotExist:
            return Response({"error": "Das Angebot mit der angegebenen ID wurde nicht gefunden."}, status=404)
