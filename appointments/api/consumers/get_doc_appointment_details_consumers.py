import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.doc_appointment_detail_serializers import DetailDoctorAppointmentSerializer
from appointments.api.serializers.serializers import ListUserAppointmentSerializer, ListDoctorAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.models import Doctor


class GetDocAppointmentDetailsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doc_appointment_detail = None

        await self.accept()

    async def receive_json(self, content):
        print("GetDocAppointmentDetailsConsumer: receive_json")
        command = content.get("command", None)
        doctor_id = content.get("doctor_id", None)
        appointment_id = content.get("appointment_id", None)
        data = content.get("data", None)

        try:
            if command == "get_doc_appointment_detail":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(doctor_id))

                self.user = await get_user(doctor_id)
                self.room_group_name = 'get_doc_appointment_detail_%s' % doctor_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_doc_appointment_detail(doctor_id, data, appointment_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_doc_appointment_detail_message',
                        'get_doc_appointment_detail_message': self.doc_appointment_detail
                    }
                )
        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################
    async def get_doc_appointment_detail_message(self, event):
        get_doc_appointment_detail_message = event['get_doc_appointment_detail_message']
        # Send message to WebSocket
        await self.send_json({
            "get_doc_appointment_detail_message": get_doc_appointment_detail_message
        })

    async def get_doc_appointment_detail(self, doctor_id, data, appointment_id):

        print(" GET APPOINTMENT: get_all_doc_appointments")
        #is_auth = is_authenticated(self.user)
        try:
            appointment_detail = await get_doc_appointment_detail_or_error(doctor_id, data, appointment_id)
            self.doc_appointment_detail = json.loads(appointment_detail)
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
def get_doc_appointment_detail_or_error(doctor_id, data, appointment_id):

    #doctor = Doctor.objects.get(user=doctor_id)
    try:
        user_appointment = Appointment.objects.get(id=appointment_id)
        serializers = DetailDoctorAppointmentSerializer(user_appointment, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")