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


class AppointmentMessageConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None
        self.user_id = None


        await self.accept()


    async def receive_json(self, content):
        print("AppointmentMessageConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        room = content.get("room", None)
        message = content.get("message", None)
        files = content.get("files", None)
        page_number = content.get("page_number", None)

        # self.user_id = user_id

        ####################
        #### CONNECT APPOINTMENT MESSAGE
        ####################

        try:
            if command == "join":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: PAGE NUMBER: " + str(room))

                self.user = await get_user(user_id)

                await self.join_room(room, user_id, page_number)

            elif command == "get_next_page":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: PAGE NUMBER: " + str(room))

                self.user = await get_user(user_id)

                await self.get_next_page(room, user_id, page_number)

            elif command == "leave":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                # Leave the room
                await self.leave_room(content["room"])

            elif command == "get_room_chat_messages":
                room_obj = await get_room_or_error(content['room'])
                payload = await get_room_chat_messages(room_obj)


                if payload != None:
                    payload = json.loads(payload)
                    await self.send_messages_payload(payload)
                else:
                    raise ClientError(204, "Something went wrong retrieving the chatroom messages.")

            elif command == "send":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: MESSAGE: " + str(message))


                await self.send_room(content["room"], content["user_id"], content["message"], content["files"])
                # raise ClientError(422,"You can't send an empty message.")

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

    async def join_room(self, room_id, user_id, page_number):
        """
        Called by receive_json when someone sent a join command.
        """
        print("TeamAsaaseConsumer: join_room")
        # is_auth = is_authenticated(self.user)

        try:
            room = await get_room_or_error(room_id)
        except ClientError as e:
            await self.handle_client_error(e)

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
                room.group_name,
                self.channel_name,
            )

        ## Add user to "users" list for room
        # if is_auth:
        await connect_user(room_id, user_id)
        #
        ## Store that we're in the room
        self.room_id = room.id
        payload = await get_room_chat_messages(room, page_number)

        payload = json.loads(payload)
        new_page_number = await get_new_page_number(room, page_number)
        num_connected_users = await get_num_connected_users(room_id)


        # await self.send_messages_payload(payload)
        # Instruct their client to finish opening the room
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "send_messages_payload",
                "messages": payload,
                "connected_user_count": num_connected_users,
                "new_page_number": new_page_number
            }
        )

    async def get_next_page(self, room_id, user_id, page_number):
        """
        Called by receive_json when someone sent a join command.
        """
        print("AppointmentMessageConsumers: join_room")
        # is_auth = is_authenticated(self.user)

        try:
            room = await get_room_or_error(room_id)
        except ClientError as e:
            await self.handle_client_error(e)

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
                room.group_name,
                self.channel_name,
            )

        ## Add user to "users" list for room
        # if is_auth:
        await connect_user(room_id, user_id)
        #
        ## Store that we're in the room
        self.room_id = room.id
        payload = await get_next_page_messages(room, page_number)

        payload = json.loads(payload)
        new_page_number = await get_new_page_number(room, page_number)
        num_connected_users = await get_num_connected_users(room_id)


        # await self.send_messages_payload(payload)
        # Instruct their client to finish opening the room
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "send_messages_payload",
                "messages": payload,
                "connected_user_count": num_connected_users,
                "new_page_number": new_page_number
            }
        )

    ### send the new user count to the room
        #num_connected_users = await get_num_connected_users(room_id)
        #await self.channel_layer.group_send(
        #    room.group_name,
        #    {
        #        "type": "connected.user.count",
        #        "connected_user_count": num_connected_users,
        #    }
        #)

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        print("AppointmentMessageConsumers: leave_room")
        # is_auth = is_authenticated(self.scope["user"])
        room = await get_room_or_error(room_id)

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

        # Remove user from "users" list
        # if is_auth:
        await disconnect_user(room_id, self.user)

        # Remove that we're in the room
        self.room_id = None

        payload = await get_room_chat_messages(room)

        payload = json.loads(payload)
        num_connected_users = await get_num_connected_users(room_id)

        # await self.send_messages_payload(payload)
        # Instruct their client to finish opening the room
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "send_messages_payload",
                "messages": payload,
                "connected_user_count": num_connected_users,
            }
        )

       # # send the new user count to the room
       # num_connected_users = await get_num_connected_users(room_id)
       # await self.channel_layer.group_send(
       #     room.group_name,
       #     {
       #         "type": "connected.user.count",
       #         "connected_user_count": num_connected_users,
       #     }
       # )

    async def send_room(self, room_id, user_id, message, files):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        print("AppointmentMessageConsumers: send_room")
        #if self.room_id != None:
        #    if str(room_id) != str(self.room_id):
        #        raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        #    if not is_authenticated(self.user):
        #        raise ClientError("AUTH_ERROR", "You must be authenticated to chat.")
        #else:
        #    raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
#
        # Get the room and send to the group about it
        try:
            room = await get_room_or_error(room_id)
        except ClientError as e:
            await self.handle_client_error(e)

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name
        )

        #self.room_id = room.id
        message_data = await create_public_room_chat_message(room_id, user_id, message, files)

        if message_data != None:
            payload = json.loads(message_data)
            #await self.send_messages_payload(payload)


            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.message",
                    "messages": payload,
                }
            )
        else:
            raise ClientError(204, "Something went wrong retrieving the chatroom messages.")


    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("AppointmentMessageConsumers: chat_message from user #")
        await self.send_json(
            {
                "messages": event["messages"],
            },
        )

    async def send_messages_payload(self, event):
        """
        Send a payload of messages to the ui
        """
        print("AppointmentMessageConsumers: send_messages_payload. ")

        await self.send_json(
            {
                "messages": event['messages'],
                "connected_user_count": event["connected_user_count"],
                "new_page_number": event["new_page_number"]
            },
        )

    async def connected_user_count(self, event):
        """
        Called to send the number of connected users to the room.
        This number is displayed in the room so other users know how many users are connected to the chat.
        """
        # Send a message down to the client
        print("AppointmentMessageConsumers: connected_user_count: count: " + str(event["connected_user_count"]))
        await self.send_json(
            {
                "connected_user_count": event["connected_user_count"]
            },
        )


@database_sync_to_async
def get_room_or_error(room_id):
    """
	Tries to fetch a room for the user
	"""
    try:
        room = PrivateChatRoom.objects.get(pk=room_id)
    except PrivateChatRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")
    return room


@database_sync_to_async
def connect_user(room_id, user_id):
    try:
        message_room = PrivateChatRoom.objects.get(id=room_id)
        if message_room != None:
            message_room.connect_user(user_id)
            count = len(message_room.connected_users.all())
            print(count)

        # return json.dumps(team_count)

    except PrivateChatRoom.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def disconnect_user(room_id, user_id):
    try:
        message_room = PrivateChatRoom.objects.get(id=room_id)
        if message_room != None:
            message_room.users.remove(user_id)
            count = len(message_room.users.all())
            print(count)

        # return json.dumps(team_count)

    except PrivateChatRoom.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


# return room.connect_user(user)

@database_sync_to_async
def get_num_connected_users(room_id):
    try:
        message_room = PrivateChatRoom.objects.get(id=room_id)
        if message_room != None:
            count = len(message_room.connected_users.all())
            print(count)
            return count

    except PrivateChatRoom.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def get_room_chat_messages(room, page_number):
    try:
        qs = PrivateRoomChatMessage.objects.by_room(room)

        p = Paginator(qs, 20)

        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_page_number = new_page_number + 1

        serializers = PrivateChatRoomMessageSerializer(p.page(page_number).object_list, many=True)
        if serializers:
            data = serializers.data

            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

@database_sync_to_async
def get_next_page_messages(room, page_number):
    try:
        qs = PrivateRoomChatMessage.objects.by_room(room)

        p = Paginator(qs, 20)

        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_page_number = new_page_number + 1

        serializers = PrivateChatRoomMessageSerializer(p.page(page_number).object_list, many=True)
        if serializers:
            data = serializers.data

            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def get_new_page_number(room, page_number):
    try:
        qs = PrivateRoomChatMessage.objects.by_room(room)

        p = Paginator(qs, 20)

        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_new_page_number = new_page_number + 1
            if new_page_number == p.num_pages:
                return "No more messages"
            return json.dumps(new_new_page_number)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")



@database_sync_to_async
def create_public_room_chat_message(room_id, user_id, message, files):

    user_obj = User.objects.get(id=user_id)

    room_obj = PrivateChatRoom.objects.get(id=room_id)

    message = PrivateRoomChatMessage.objects.create(
        user=user_obj,
        room=room_obj,
        message=message
    )
    message.save()

    if files != None:
        for file in files:
            file_file = base64_file(file['file'], file['file_name'], file['file_ext'])
            new_file = File.objects.create(name=file['file_name'], file=file_file, user=user_obj)
            message.files.add(new_file)
            message.save()

    try:
        qs = PrivateRoomChatMessage.objects.by_room(room_id)
        p = Paginator(qs, 20)

        serializers = PrivateChatRoomMessageSerializer(p.page(1).object_list, many=True)
        if serializers:
            data = serializers.data
            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


def base64_file(data, name, ext):
    print("############## DAAATAAAAAA")
    file = ContentFile(base64.b64decode(data), name=name+ext)
    return file


