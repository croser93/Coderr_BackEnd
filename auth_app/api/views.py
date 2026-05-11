from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token'     :   token.key,
                'username'  :   saved_account.get_(),
                'email'     :   saved_account.email,
                'user_id'   :   saved_account.id
            }
        else:
             return Response(serializer.errors, status=400)

        return Response(data, status=201)
