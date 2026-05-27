from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import UserOrAdmin


from profile_app.models import ProfileModel
from .serializers import ProfileSerializer, ProfilesBusinessSerializer, ProfilesCustomersSerializer

class ProfileListView(APIView):
    """
    View List for User Profile.
    
    Endpoints:
    - GET /api/profile/ - List all profile.

    """

    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        profile_list = ProfileModel.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return Response (serializer.data)
    
class ProfileDetailView(APIView):
    """
    View single User Profile.
    
    Endpoints:
    - GET /api/profile/{ID} - Single profile where user is a member
    - PATCH /api/profile/{ID} - Update a signle profile
    - DELETE /api/profile/{ID} - Delete a single profile
    
    """
    
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
    
    """
    View List User Profile.
    
    Endpoints:
    - GET /api/profile//business/ - List of profile where user is business user.
    
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile_list = ProfileModel.objects.filter(user__profile__type="customer")
        serializer = ProfilesCustomersSerializer(profile_list, many=True)
        return Response (serializer.data)

        
class ProfileBusinessListView(APIView):
    """
    View List User Profile.
    
    Endpoints:
    - GET /api/profile/customer/ - List profile where user is customer user.

    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile_list = ProfileModel.objects.filter(user__profile__type="business")
        serializer = ProfilesBusinessSerializer(profile_list, many=True)
        return Response (serializer.data)