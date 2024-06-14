from django.contrib.auth import get_user_model
from rest_framework import serializers

from communications.models import PrivateRoomChatMessage, PrivateChatRoom
from file_management.models import File
from user_profile.models import PersonalInfo

User = get_user_model()


class ChatRoomFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'file_ext', 'file_size']



class ChatRoomPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo']


class ChatRoomUserSerializer(serializers.ModelSerializer):
    personal_info = ChatRoomPersonalInfoSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info']


class PrivateChatRoomMessageSerializer(serializers.ModelSerializer):
    user = ChatRoomUserSerializer()
    files = ChatRoomFileSerializer(many=True)

    class Meta:
        model = PrivateRoomChatMessage
        fields = ['id', 'message', 'files', 'room', 'user', 'timestamp']




class PrivateChatRoomSerializer(serializers.ModelSerializer):
    user1 = ChatRoomUserSerializer()
    user2 = ChatRoomUserSerializer()

    class Meta:
        model = PrivateChatRoom
        fields = ['id', 'user1', 'user2']


