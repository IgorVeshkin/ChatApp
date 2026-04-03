from django.db import models

import uuid

from django.contrib.auth.models import User


def chat_image_path_setter(instance, filename):
    return 'chatroom__{0}/cover__{1}'.format(instance.title, filename)

class Chatroom(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="Название чата")
    description = models.TextField(blank=True, null=True)
    coverImage = models.ImageField(upload_to=chat_image_path_setter, blank=True, null=True)

    users_list = models.ManyToManyField(User, verbose_name='Участники', related_name="users")

    created_by = models.ForeignKey(User, verbose_name='Создал', on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'\'{self.uuid}\' -> {self.title} | {self.created_by}'