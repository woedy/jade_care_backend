import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.api.serializers.serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.patient_serializers.patient_profile_serializer import PatientProfileSerializer

User = get_user_model()

class GetPatientProfileConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.patient_profile = None


        await self.accept()

    async def receive_json(self, content):
        print("GetPatientProfileConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_patient_profile":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_patient_profile_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_patient_profile(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_patient_profile_message',
                        'get_patient_profile_message': self.patient_profile
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND PATIENT MESSAGE
    ####################

    async def get_patient_profile_message(self, event):
        get_patient_profile_message = event['get_patient_profile_message']
        # Send message to WebSocket
        await self.send_json({
            "get_patient_profile_message": get_patient_profile_message
        })

    async def get_patient_profile(self, user_id, data):

        print(" PATIENT PROFILE: get_patient_profile")
        #is_auth = is_authenticated(self.user)
        try:
            profile = await get_patient_profile_or_error(user_id, data)
            self.patient_profile = json.loads(profile)
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
def get_patient_profile_or_error(user_id, data):

    try:
        user = User.objects.get(id=user_id)

        serializers = PatientProfileSerializer(user, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except User.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

