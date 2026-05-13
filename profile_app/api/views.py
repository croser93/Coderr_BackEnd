from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import UserOrAdmin


from profile_app.models import ProfileModel
from .serializers import ProfileSerializer

class ProfileListView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile_list = ProfileModel.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return Response (serializer.data)
    
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, UserOrAdmin]
    
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
            self.check_object_permissions(request, profile)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except ProfileModel.DoesNotExist:
            return Response ({"error" : "Das Benutzerprofil wurde nicht gefunden."}, status=404)
        
class ProfileCustomerListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile_list = ProfileModel.objects.filter(user__profile__type="customer")
        serializer = ProfileSerializer(profile_list, many=True)
        return Response (serializer.data)

        
class ProfileBusinessListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile_list = ProfileModel.objects.filter(user__profile__type="business")
        serializer = ProfileSerializer(profile_list, many=True)
        return Response (serializer.data)