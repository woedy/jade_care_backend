import base64
import codecs
import json
import imghdr

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from communications.api.serializers.appointment_message_serializer import PrivateChatRoomMessageSerializer
from communications.models import PrivateChatRoom, PrivateRoomChatMessage
from file_management.models import File
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user, is_authenticated


User = get_user_model()


class ChatMessagesAdminConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room = None
        self.room_group_name = None
        self.user_id = None


        await self.accept()


    async def receive_json(self, content):
        print("ChatMessagesAdminConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        room = content.get("room", None)
        message = content.get("message", None)
        files = content.get("files", None)
        page_number = content.get("page_number", None)



        try:
            if command == "send":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: MESSAGE: " + str(message))
                self.room_group_name = 'chat_message_%s' % content["room"]

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.send_room(content["room"], content["user_id"], content["message"], content["files"])

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'room_messages',
                        'room_messages': self.room
                    }
                )


        except ClientError as e:
            await self.handle_client_error(e)

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # leave the room
        print("AppointmentMessageConsumers: disconnect")
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception:
            pass

    async def handle_client_error(self, e):
        """
        Called when a ClientError is raised.
        Sends error data to UI.
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return

    async def send_room(self, room, user_id, message, files):

        print(" send_room: send_room")
        # is_auth = is_authenticated(self.user)
        try:
            room = await send_room_or_error(room, user_id, message, files)
            self.room = json.loads(room)
        except ClientError as e:
            await self.handle_client_error(e)


    async def room_messages(self, event):
        room_messages = event['room_messages']
        # Send message to WebSocket
        await self.send_json({
            "room_messages": room_messages
        })


@database_sync_to_async
def send_room_or_error(room, user_id, message, files):
    user = User.objects.get(id=user_id)
    c_room = PrivateChatRoom.objects.get(id=room)
    try:
        message = PrivateRoomChatMessage.objects.create(
            user=user,
            room=c_room,
            message=message,
        )
        message.save()

        new_messages = PrivateRoomChatMessage.objects.all().filter(room=c_room).order_by('timestamp')



        serializers = PrivateChatRoomMessageSerializer(new_messages, many=True)
        if serializers:
            data = serializers.data
            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")








