
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BaseInfoSerializer

class BaseInfoView(APIView):
    """
    View  for return Base Information of the site Coderr.
    
    Endpoints:
    - GET /api/base-info/ 
    """

    def get(self,request):
        serializer = BaseInfoSerializer({})
        return Response(serializer.data, status=200)
    