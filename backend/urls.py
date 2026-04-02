from django.urls import path

from . views import BasicResponse

urlpatterns = [
    path('', BasicResponse.as_view(), name="basic_response"),
]