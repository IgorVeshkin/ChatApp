from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class BasicResponse(APIView):

    def get(self, request):

        return Response({'message': 'If you see this message than everything works correct!'})
