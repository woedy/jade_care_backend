import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.models import Doctor
from user_profile.doctor_serializers.list_doc_serializer import ListDoctorsSerializer

User = get_user_model()

class ListDoctorsConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doctors = None


        await self.accept()

    async def receive_json(self, content):
        print("ListDoctorsConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "list_all_doctors":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'list_doctors_profile_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.list_all_doctors(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'list_doctors_message',
                        'list_doctors_message': self.doctors
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND DOCTORS MESSAGE
    ####################

    async def list_doctors_message(self, event):
        list_doctors_message = event['list_doctors_message']
        # Send message to WebSocket
        await self.send_json({
            "list_doctors_message": list_doctors_message
        })

    async def list_all_doctors(self, user_id, data):

        print(" PATIENT PROFILE: get_patient_profile")
        #is_auth = is_authenticated(self.user)
        try:
            doctors = await list_all_doctors_or_error(user_id, data)
            self.doctors = json.loads(doctors)
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
def list_all_doctors_or_error(user_id, data):

    try:
        doctors = Doctor.objects.all().order_by('id')

        serializers = ListDoctorsSerializer(doctors, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Doctor.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

