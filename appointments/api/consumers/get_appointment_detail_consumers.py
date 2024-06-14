import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.appointment_detail_serializers import AppointmentDetailSerializer
from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user


class GetAppointmentDetailConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.appointment_detail = None


        await self.accept()

    async def receive_json(self, content):
        print("GetAppointmentDetailConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)
        appointment_id = content.get("appointment_id", None)

        try:
            if command == "get_appointment_detail":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_appointment_detail_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_appointment_detail(user_id, data, appointment_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_appointment_detail_message',
                        'get_appointment_detail_message': self.appointment_detail
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################

    async def get_appointment_detail_message(self, event):
        get_appointment_detail_message = event['get_appointment_detail_message']
        # Send message to WebSocket
        await self.send_json({
            "get_appointment_detail_message": get_appointment_detail_message
        })

    async def get_appointment_detail(self, user_id, data, appointment_id):

        print(" PROJECT DETAIL: get_appointment_detail")
        #is_auth = is_authenticated(self.user)
        try:
            appointment_detail = await get_appointment_detail_or_error(user_id, data, appointment_id)
            self.appointment_detail = json.loads(appointment_detail)
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
def get_appointment_detail_or_error(user_id, data, appointment_id):

    try:
        appointment_detail = Appointment.objects.get(id=appointment_id)
        serializers = AppointmentDetailSerializer(appointment_detail, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

