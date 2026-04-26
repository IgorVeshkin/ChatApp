from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from . models import Chatroom

from . serializers import ChatroomSerializer

from rest_framework.permissions import IsAuthenticated


class BasicResponse(APIView):

    def get(self, request):

        return Response({'message': 'If you see this message than everything works correct!'})


class ChatroomResponse(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        
        # Тестовый uuid созданной записе в базе данных 
        chatroom = Chatroom.objects.get(pk="1991f68f-693d-4e95-bd32-7e52d6afbfe9")
        
        return Response({"chatroom": ChatroomSerializer(chatroom).data})


class CheckAuthResponse(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        return Response({
            "is_auth": not request.user.is_anonymous, 
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            }, status=HTTP_200_OK)
