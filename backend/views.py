from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from . models import Chatroom

from . serializers import ChatroomSerializer

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate


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

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "is_auth": not request.user.is_anonymous, 
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            }, status=HTTP_200_OK)



class TokenObtainPairCookieView(APIView):
    """
        Получение access и refresh токенов через httpOnly куки 
    """
    def post(self, request, *args, **kwargs):

        # request.data возвращает структуру: {'username': 'Логин', 'password': 'Пароль'}

        user = authenticate(username=request.data["username"], password=request.data["password"])

        # Если пользователь не нашелся
        if user is None:
            print("We are here:", user)
            return Response({"error": "Invalid credentials. User is not found"}, status=404)

        
        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response = Response({"message": "Tokens have been received and set in cookies"})

        # Lax doesn't work for localhost cross-origin Websockets (if frotend is localhost:5173 and backend is localhost:800)
        # Use samesite="None" and secure="False" for only development

        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax', # Lax if secure=False, if None when has to be secure=True 
            max_age=60*10  # 10 minutes token lifetime
        )

        response.set_cookie(
            key='refresh',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax', # Lax if secure=False, if None when has to be secure=True 
            max_age=60*60*8  # 8 hour token lifetime
        )

        return response


class TokenRefreshCookieView(APIView):
    """
        Обновление access-токена через refresh токен и последующая замена access-токена в httpOnly куках
    """

    def post(self, request, *args, **kwargs):

        # Пример токена обновления: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ.........
        
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token is None:
            return Response({"error": "Refresh token is missing"}, status=401)

        
        from rest_framework_simplejwt.serializers import TokenRefreshSerializer
        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        new_access_token = serializer.validated_data['access']

        response = Response({"message": "Access token has been successfully refreshed and set in cookies"})

        response.set_cookie(
            key='access',
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite='Lax', # Lax if secure=False, if None when has to be secure=True 
            max_age=60*10 # 10 minutes token lifetime
        )

        return response


class CookieLogoutView(APIView):
    """
        Выход из аккаунта путем очистки access и refresh токенов из куков
    """
    def post(self, request, *args, **kwargs):

        response = Response({"message": "User has been successfully logged out"})
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
