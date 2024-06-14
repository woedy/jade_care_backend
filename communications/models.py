from django.conf import settings
from django.db import models

from file_management.models import File

class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user1', null=True,
                              blank=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user2', null=True,
                              blank=True)

    connected_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="connected_users")
    is_active = models.BooleanField(default=False)

    def connect_user(self, user):
        is_user_added = False
        if not user is self.connected_users.all():
            self.connected_users.add(user)
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.connected_users.all():
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f"PrivateChatRoom-{self.id}"


class RoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PrivateRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class PrivateRoomChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="private_chat_room_messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(unique=False, blank=False)
    files = models.ManyToManyField(File, default=None, blank=True, related_name='private_message_files')


    objects = RoomChatMessageManager()

    def __str__(self):
        return self.message
