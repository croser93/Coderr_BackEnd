from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class RegistrationView(APIView):
    """
    View  for create a new User for Kanban board.
    
    Endpoints:
    - POST /api/registration/ - Create a new bUser.
    """
    permission_classes = [AllowAny]
    

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token'     :   token.key,
                'username'  :   saved_account.username,
                'email'     :   saved_account.email,
                'user_id'   :   saved_account.id
            }
        else:
            return Response(serializer.errors, status=400)
        return Response(data, status=201)
    

class LoginView(APIView):
    """
    View for Log in in the Kanban board.
    
    Endpoints:
    - POST /api/login/ - The user is logged in, and the token is created.
    """
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token'     :   token.key,
                'username'  :   user.username,
                'email'     :   user.email,
                'user_id'   :   user.id
            }
        else:
            return Response(serializer.errors, status=400)
        return Response(data, status=200)
    
class LogoutView(APIView):
    """
    View for Log out from the Kanban board.
    
    Endpoints:
    - POST /api/logout/ - The user is logged out, and the token is deleted.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logout erfolgreich. Token wurde gelöscht.'}, status=200)
    
    
    
    
