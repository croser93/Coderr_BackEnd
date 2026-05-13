
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OfferPostSerializer, OfferGetSerializer
from offers_app.models import OfferModel
from rest_framework.permissions import IsAuthenticated




class OfferListView(APIView):

    permission_classes = [IsAuthenticated]

    
    def post(self, request):
        serializer = OfferPostSerializer(data=request.data)
        if serializer.is_valid():
            saved_offer = serializer.save(user=request.user)
            return Response(OfferPostSerializer(saved_offer).data, status=201)
        else:
             return Response(serializer.errors, status=400)
        
    def get(self, request):
        offer = OfferModel.objects.all()
        serializer = OfferGetSerializer(offer, many=True)
        return Response (serializer.data)



