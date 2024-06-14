import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from prescriptions.api.serializers.serializers import ListPrescriptionsSerializer
from prescriptions.models import Prescription
from user_profile.models import Doctor, Patient

User = get_user_model()

class ListPrescriptionsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.user_appointments = None
        self.patient_prescriptions = None


        await self.accept()

    async def receive_json(self, content):
        print("ListPrescriptionsConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "list_prescriptions":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'list_prescriptions_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.list_prescriptions(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'list_prescriptions_message',
                        'list_prescriptions_message': self.patient_prescriptions
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND PRESCRIPTIONS MESSAGE
    ####################

    async def list_prescriptions_message(self, event):
        list_prescriptions_message = event['list_prescriptions_message']
        # Send message to WebSocket
        await self.send_json({
            "list_prescriptions_message": list_prescriptions_message
        })

    async def list_prescriptions(self, user_id, data):

        print(" PRESCRIPTION: list_prescriptions")
        #is_auth = is_authenticated(self.user)
        try:
            prescriptions = await list_prescriptions_or_error(user_id, data)
            self.patient_prescriptions = json.loads(prescriptions)
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
def list_prescriptions_or_error(user_id, data):


    user = User.objects.get(id=user_id)

    try:
        prescriptions = Prescription.objects.filter(patient=user).order_by('-id')
        serializers = ListPrescriptionsSerializer(prescriptions, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Prescription.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")
