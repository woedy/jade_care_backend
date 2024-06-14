import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user


class GetAppointmentConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.user_appointments = None


        await self.accept()

    async def receive_json(self, content):
        print("GetAppointmentConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_appointments":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_appointment_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_all_user_appointment(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_all_appointments_message',
                        'get_all_appointments_message': self.user_appointments
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################

    async def get_all_appointments_message(self, event):
        get_all_appointments_message = event['get_all_appointments_message']
        # Send message to WebSocket
        await self.send_json({
            "get_all_appointments_message": get_all_appointments_message
        })

    async def get_all_user_appointment(self, user_id, data):

        print(" PROJECT DETAIL: get_project_detail")
        #is_auth = is_authenticated(self.user)
        try:
            appointments = await get_all_user_appointment_or_error(user_id, data)
            self.user_appointments = json.loads(appointments)
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
def get_all_user_appointment_or_error(user_id, data):

    try:
        user_appointments = Appointment.objects.filter(patient=user_id).order_by('-id')
        serializers = ListUserAppointmentSerializer(user_appointments, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

