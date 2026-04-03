from rest_framework import serializers

from .models import Chatroom

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name")

class ChatroomSerializer(serializers.ModelSerializer):

    users_list = UserSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = Chatroom
        fields = ("uuid", "title", "description", "coverImage", "users_list", "created_by")