import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.api.serializers.serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.doctor_serializers.doctor_profile_serializer import DoctorProfileSerializer
from user_profile.patient_serializers.patient_profile_serializer import PatientProfileSerializer

User = get_user_model()

class GetDoctorProfileConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doctor_profile = None


        await self.accept()

    async def receive_json(self, content):
        print("GetDoctorProfileConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_doctor_profile":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_doctor_profile_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_doctor_profile(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_doctor_profile_message',
                        'get_doctor_profile_message': self.doctor_profile
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND DOCTOR MESSAGE
    ####################

    async def get_doctor_profile_message(self, event):
        get_doctor_profile_message = event['get_doctor_profile_message']
        # Send message to WebSocket
        await self.send_json({
            "get_doctor_profile_message": get_doctor_profile_message
        })

    async def get_doctor_profile(self, user_id, data):

        print(" DOCTOR PROFILE: get_doctor_profile")
        #is_auth = is_authenticated(self.user)
        try:
            profile = await get_doctor_profile_or_error(user_id, data)
            self.doctor_profile = json.loads(profile)
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
def get_doctor_profile_or_error(user_id, data):

    try:
        user = User.objects.get(id=user_id)

        serializers = DoctorProfileSerializer(user, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except User.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

