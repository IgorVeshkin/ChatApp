from django.urls import path

from . views import BasicResponse, ChatroomResponse

urlpatterns = [
    path('', BasicResponse.as_view(), name="basic_response"),
    path('chatroom/', ChatroomResponse.as_view(), name="chatroom_data_response"),
]