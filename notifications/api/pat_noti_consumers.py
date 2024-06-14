import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from notifications.api.serializers import ListNotificationSerializer, ListDocNotificationSerializer, \
    ListPatNotificationSerializer
from notifications.models import Notification


User = get_user_model()

class PatientNotificationConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.patinet_notifications = None


        await self.accept()

    async def receive_json(self, content):
        print("PatientNotificationConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)
        notification_id = content.get("notification_id", None)

        try:
            if command == "get_notifications":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_notifications_pat_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_all_notifications(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_all_notifications_message',
                        'get_all_notifications_message': self.patinet_notifications
                    }
                )

            if command == "set_read_notification":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: NOTIFICATION ID: " + str(notification_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_notifications_pat_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.set_read_notification(user_id, notification_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_all_notifications_message',
                        'get_all_notifications_message': self.patinet_notifications
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND NOTIFICATION MESSAGE
    ####################

    async def get_all_notifications_message(self, event):
        get_all_notifications_message = event['get_all_notifications_message']
        # Send message to WebSocket
        await self.send_json({
            "get_all_notifications_message": get_all_notifications_message
        })

    async def get_all_notifications(self, user_id, data):

        print(" NOTIFICATIOIN: get_all_notifications_message")
        #is_auth = is_authenticated(self.user)
        try:
            notifications = await get_all_notifications_or_error(user_id, data)
            self.patinet_notifications = json.loads(notifications)
        except ClientError as e:
            await self.handle_client_error(e)

    async def set_read_notification(self, user_id, notification_id):

        print(" NOTIFICATIOIN: get_all_notifications_message")
        #is_auth = is_authenticated(self.user)
        try:
            notifications = await set_read_notification_or_error(user_id, notification_id)
            self.patinet_notifications = json.loads(notifications)
        except ClientError as e:
            await self.handle_client_error(e)

    async def handle_client_error(self, e):
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return


@database_sync_to_async
def get_all_notifications_or_error(user_id, data):

    print("USER IIIDDD")
    print(user_id)

    user = User.objects.get(id=user_id)
    print(user)

    try:
        notifications = Notification.objects.filter(patient=user).order_by('-timestamp')
        serializers = ListNotificationSerializer(notifications, many=True)

        if serializers:
            data = serializers.data
            print(data)
            return json.dumps(data)
    except Notification.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")





@database_sync_to_async
def set_read_notification_or_error(user_id, notification_id):

    print("USER IIIDDD")
    print(user_id)

    user = User.objects.get(id=user_id)
    print(user)

    try:
        notification = Notification.objects.get(id=notification_id)

        if notification.pat_read == False:
            notification.pat_read = True
            notification.save()


        notifications = Notification.objects.filter(patient=user).order_by('-timestamp')
        serializers = ListPatNotificationSerializer(notifications, many=True)

        if serializers:
            data = serializers.data
            print(data)
            return json.dumps(data)
    except Notification.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")





