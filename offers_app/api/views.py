
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OfferPostSerializer, OfferGetSerializer
from offers_app.models import OfferModel
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUserOrAdmin



class OfferListView(APIView):

    permission_classes = [IsAuthenticated, IsBusinessUserOrAdmin]

    
    def post(self, request):
        try:
            serializer = OfferPostSerializer(data=request.data)
            self.check_permissions(request, serializer)
            if serializer.is_valid():
                saved_offer = serializer.save(user=request.user)
                return Response(OfferPostSerializer(saved_offer).data, status=201)
            else:
                return Response(serializer.errors, status=400)
        except: 
         return Response({'error':'Authentifizierter Benutzer ist kein `business` Profil'}, status=403)
        
    def get(self, request):
        offer = OfferModel.objects.all()
        serializer = OfferGetSerializer(offer, many=True)
        return Response (serializer.data)



