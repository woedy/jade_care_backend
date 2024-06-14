import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from prescriptions.api.serializers.serializers import ListPrescriptionsSerializer
from prescriptions.models import Prescription
from user_profile.models import Doctor, Patient

User = get_user_model()

class AddPrescriptionsConsumer(AsyncJsonWebsocketConsumer):

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
        print("AddPrescriptionsConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "add_prescription":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'add_prescription_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.add_prescriptions(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'add_prescriptions_message',
                        'add_prescriptions_message': self.patient_prescriptions
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND PRESCRIPTIONS MESSAGE
    ####################

    async def add_prescriptions_message(self, event):
        add_prescriptions_message = event['add_prescriptions_message']
        # Send message to WebSocket
        await self.send_json({
            "add_prescriptions_message": add_prescriptions_message
        })

    async def add_prescriptions(self, user_id, data):

        print(" PRESCRIPTION:add_prescriptions")
        #is_auth = is_authenticated(self.user)
        try:
            prescriptions = await add_prescription_or_error(user_id, data)
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
def add_prescription_or_error(user_id, data):
    print(data)
    user = User.objects.get(id=user_id)


    appointment_id = data["appointment"]
    medication_name = data["medication_name"]
    generic_name = data["generic_name"]
    dosage = data["dosage"]
    frequency = data["frequency"]
    instructions = data["instructions"]
    patient = data["patient"]

    appointment = Appointment.objects.get(id=appointment_id)
    patient_ = appointment.patient


    try:
        prescription = Prescription.objects.create(
            appointment=appointment,
            medication_name=medication_name,
            generic_name=generic_name,
            dosage=dosage,
            frequency=frequency,
            instructions=instructions,
            patient=patient_
        )
        prescription.save()

        prescriptions = Prescription.objects.filter(patient=user).order_by('-id')
        serializers = ListPrescriptionsSerializer(prescriptions, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Prescription.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

