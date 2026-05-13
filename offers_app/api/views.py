
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OfferPostSerializer


class OfferListView(APIView):
    
    def post(self, request):
        serializer = OfferPostSerializer(data=request.data)
        if serializer.is_valid():
            saved_offer = serializer.save()
            return Response(OfferPostSerializer(saved_offer).data, status=201)
        else:
             return Response(serializer.errors, status=400)



