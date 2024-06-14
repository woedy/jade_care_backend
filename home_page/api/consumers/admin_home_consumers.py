import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.models import Appointment
from home_page.api.doc_home_serializers import ListDocAppointmentHomeSerializer
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from notifications.models import Notification
from user_profile.models import PersonalInfo, Doctor

User = get_user_model()

class GetAdminHomeDataConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.admin_profile = None


        await self.accept()

    async def receive_json(self, content):
        print("GetAdminHomeDataConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_home_data":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_home_data_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_home_data(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_home_data_message',
                        'get_home_data_message': self.admin_profile
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND ADMIN MESSAGE
    ####################

    async def get_home_data_message(self, event):
        get_home_data_message = event['get_home_data_message']
        # Send message to WebSocket
        await self.send_json({
            "get_home_data_message": get_home_data_message
        })

    async def get_home_data(self, user_id, data):

        print(" aADMIN PROFILE: get_home_data")
        #is_auth = is_authenticated(self.user)
        try:
            profile = await get_home_data_or_error(user_id, data)
            self.admin_profile = json.loads(profile)
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
def get_home_data_or_error(user_id, data):

    try:
        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(user=user)
        personal_info = PersonalInfo.objects.get(user=user)


        print(user)
        print(user.last_name)
        print(user.first_name)
        print(doctor.title)

        user_data = {}
        user_data['doctor_id'] = doctor.id
        user_data["last_name"] = user.last_name
        user_data["first_name"] = user.first_name
        user_data['photo'] = personal_info.photo.url
        user_data['title'] = doctor.title



        notification = Notification.objects.filter(doctor=doctor.user).filter(doc_read=False).order_by('-timestamp')
        notification_count = notification.count()

        payload = {}
        payload['user_data'] = user_data
        payload['notification_count'] = notification_count

        return json.dumps(payload)

    except User.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

