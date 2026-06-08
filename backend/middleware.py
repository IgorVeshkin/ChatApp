from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from channels.db import database_sync_to_async
from urllib.parse import parse_qs


@database_sync_to_async
def get_user_from_token(token):
    try:

         validated_token = AccessToken(token)

         from django.contrib.auth import get_user_model

         user = get_user_model()

         user_id = validated_token["user_id"]

         return user.objects.get(id=user_id)

    except (TokenError, user.DoesNotExist, KeyError):

        return AnonymousUser()


class JWTCookiesAuthMiddleware:
    """
    Custom JWT middleware for Django Channels to authenticate via use of cookies.
    Expects the token as a 'token' query parameter.
    """

    def __init__(self, inner):
        self.inner = inner
    

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        scope["user"] = AnonymousUser()

        if b"cookie" in headers:
            cookies = headers[b"cookie"].decode()

            cookies_dict = dict(item.split("=") for item in cookies.split("; "))

            access_token = cookies_dict.get("access")
            refresh_token = cookies_dict.get("refresh")

            if access_token:
                user = await get_user_from_token(access_token)
                scope["user"] = user

            # Refreshing access token (No need for that, user won't be able to get to page with websocket without valid access and refresh tokens)
            
            # elif refresh_token:
            #     try:
            #         from rest_framework_simplejwt.tokens import RefreshToken

            #         new_access_token = RefreshToken(refresh_token).access_token
            #         user = await get get_user_from_token(str(new_access_token))

            #         scope["user"] = user
            #     except TokenError:
            #         pass

        return await self.inner(scope, receive, send)


def JWTCookiesAuthMiddlewareStack(inner):
    return JWTCookiesAuthMiddleware(inner)

