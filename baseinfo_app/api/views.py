
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BaseInfoSerializer

class BaseInfoView(APIView):

    def get(self,request):
        serializer = BaseInfoSerializer({})
        return Response(serializer.data, status=200)
    