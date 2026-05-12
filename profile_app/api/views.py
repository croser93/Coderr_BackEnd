from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from profile_app.models import ProfileModel
from .serializers import ProfileSerializer

class ProfileListView(APIView):
    
    def get(self, request):
        profile_list = ProfileModel.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return Response (serializer.data)