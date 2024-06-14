import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.models import Doctor
from user_profile.doctor_serializers.detail_doctor_serializer import DetailDoctorsSerializer

User = get_user_model()

class DoctorDetailConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doctor_detail = None


        await self.accept()

    async def receive_json(self, content):
        print("DoctorDetailConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        doctor_id = content.get("doctor_id", None)
        slot_id = content.get("slot_id", None)
        data = content.get("data", None)

        try:
            if command == "doctor_details":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'doctor_details_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_doctor_details(user_id, doctor_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'doctor_details_message',
                        'doctor_details_message': self.doctor_detail
                    }
                )

            if command == "delete_date_time_slot":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'doctor_details_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.delete_doctor_date_time_slot(user_id, doctor_id, data, slot_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'doctor_details_message',
                        'doctor_details_message': self.doctor_detail
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND DOCTOR MESSAGE
    ####################

    async def doctor_details_message(self, event):
        doctor_details_message = event['doctor_details_message']
        # Send message to WebSocket
        await self.send_json({
            "doctor_details_message": doctor_details_message
        })

    async def get_doctor_details(self, user_id, doctor_id, data):

        print(" DOCTOR PROFILE: get_doctor_details")
        #is_auth = is_authenticated(self.user)
        try:
            doctor_detail = await get_doctor_details_or_error(user_id, doctor_id, data)
            self.doctor_detail = json.loads(doctor_detail)
        except ClientError as e:
            await self.handle_client_error(e)

    async def delete_doctor_date_time_slot(self, user_id, doctor_id, data, slot_id):

        print(" DOCTOR PROFILE: delete_doctor_date_time_slot")
        #is_auth = is_authenticated(self.user)
        try:
            doctor_detail = await delete_doctor_date_time_slot_or_error(user_id, doctor_id, data, slot_id)
            self.doctor_detail = json.loads(doctor_detail)
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
def get_doctor_details_or_error(user_id, doctor_id,  data):

    try:
        doctor_detail = Doctor.objects.get(id=doctor_id)

        serializers = DetailDoctorsSerializer(doctor_detail)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Doctor.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")



@database_sync_to_async
def delete_doctor_date_time_slot_or_error(user_id, doctor_id,  data, slot_id):
    print(doctor_id)
    print(slot_id)

    try:
        doctor_detail = Doctor.objects.get(id=doctor_id)
        doctor_detail.available_slot.remove(slot_id)
        doctor_detail.save()

        doctor_detail = Doctor.objects.get(id=doctor_id)
        serializers = DetailDoctorsSerializer(doctor_detail)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Doctor.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

