import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.serializers import ListUserAppointmentSerializer, ListDoctorAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.models import Doctor


class GetDocAppointmentConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doc_appointments = None

        await self.accept()

    async def receive_json(self, content):
        print("GetDocAppointmentConsumer: receive_json")
        command = content.get("command", None)
        doctor_id = content.get("doctor_id", None)
        data = content.get("data", None)

        try:
            if command == "get_doc_appointment":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(doctor_id))

                self.user = await get_user(doctor_id)
                self.room_group_name = 'get_doc_appointment_%s' % doctor_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_all_doc_appointments(doctor_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_all_doc_appointments_message',
                        'get_all_doc_appointments_message': self.doc_appointments
                    }
                )
        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################
    async def get_all_doc_appointments_message(self, event):
        get_all_doc_appointments_message = event['get_all_doc_appointments_message']
        # Send message to WebSocket
        await self.send_json({
            "get_all_doc_appointments_message": get_all_doc_appointments_message
        })

    async def get_all_doc_appointments(self, doctor_id, data):

        print(" GET APPOINTMENT: get_all_doc_appointments")
        #is_auth = is_authenticated(self.user)
        try:
            appointments = await get_all_doc_appointments_or_error(doctor_id, data)
            self.doc_appointments = json.loads(appointments)
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
def get_all_doc_appointments_or_error(doctor_id, data):

    doctor = Doctor.objects.get(user=doctor_id)
    try:
        user_appointments = Appointment.objects.filter(doctor=doctor).order_by('-id')
        serializers = ListDoctorAppointmentSerializer(user_appointments, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")