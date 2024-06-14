import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.appointment_medium_serializers import AppointmentMediumsSerializer
from appointments.api.serializers.serializers import ListUserAppointmentSerializer, AppointmentForOtherSerializer
from appointments.models import Appointment, AppointmentMedium
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user


class GetAppointmentMediumConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.appointment_mediums = None


        await self.accept()

    async def receive_json(self, content):
        print("GetAppointmentMediumConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_appointment_mediums":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_appointment_mediums_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_appointment_mediums(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_appointment_mediums_message',
                        'get_appointment_mediums_message': self.appointment_mediums
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MEDIUM MESSAGE
    ####################

    async def get_appointment_mediums_message(self, event):
        get_appointment_mediums_message = event['get_appointment_mediums_message']
        # Send message to WebSocket
        await self.send_json({
            "get_appointment_mediums_message": get_appointment_mediums_message
        })

    async def get_appointment_mediums(self, user_id, data):

        print(" PROJECT DETAIL: get_appointment_mediums")
        #is_auth = is_authenticated(self.user)
        try:
            appointment_mediums = await get_appointment_mediums_or_error(user_id, data)
            self.appointment_mediums = json.loads(appointment_mediums)
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
def get_appointment_mediums_or_error(user_id, data):

    try:
        appointment_mediums = AppointmentMedium.objects.all()
        serializers = AppointmentMediumsSerializer(appointment_mediums, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

