from django.urls import path

from . views import BasicResponse, ChatroomResponse, CheckAuthResponse 

# Представляния авторизации через куки
from . views import TokenObtainPairCookieView, TokenRefreshCookieView, CookieLogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', BasicResponse.as_view(), name="basic_response"),
    path('chatroom/', ChatroomResponse.as_view(), name="chatroom_data_response"),
    path('check-auth/', CheckAuthResponse.as_view(), name="check_authentication"),

    path("login/", TokenObtainPairView.as_view(), name="login_by_jwt"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),

    # Авторизация пользователя через httpOnly cookie 
    path("login_v2/", TokenObtainPairCookieView.as_view(), name="login_by_cookies_jwt"),
    path("refresh-token_v2/", TokenRefreshCookieView.as_view(), name="refresh_cookies_token"),
    path('logout_v2/', CookieLogoutView.as_view(), name='cookies_logout'),

]