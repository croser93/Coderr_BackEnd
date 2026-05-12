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
    
class ProfileDetailView(APIView):
    
    def get(self, request, pk):
        try:
            profile = ProfileModel.objects.get(user_id=pk)
            serializer = ProfileSerializer(profile)
            return Response (serializer.data, status=200)
        except ProfileModel.DoesNotExist:
            return Response ({"error" : "Das Benutzerprofil wurde nicht gefunden."}, status=404)
        
    def patch(self, request, pk):
        try:
            profile = ProfileModel.objects.get(user_id=pk)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except ProfileModel.DoesNotExist:
            return Response ({"error" : "Das Benutzerprofil wurde nicht gefunden."}, status=404)

        