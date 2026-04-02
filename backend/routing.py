from django.urls import path

from .consumers import ChatroomConsumer

ws_urlpatterns = [
    path("ws/testing/", ChatroomConsumer.as_asgi()),
]