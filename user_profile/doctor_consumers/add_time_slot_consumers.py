import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.api.serializers.serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.doctor_serializers.doctor_profile_serializer import DoctorProfileSerializer, \
    ListAppointmentSlotSerializer
from user_profile.models import AppointmentSlot, Doctor, TimeSlot
from user_profile.patient_serializers.patient_profile_serializer import PatientProfileSerializer

User = get_user_model()

class AddTimeSlotConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doctor_time_slots = None


        await self.accept()

    async def receive_json(self, content):
        print("AddTimeSlotConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "add_time_slot":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'add_time_slot_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.add_time_slot(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'add_time_slot_message',
                        'add_time_slot_message': self.doctor_time_slots
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND DOCTOR MESSAGE
    ####################

    async def add_time_slot_message(self, event):
        add_time_slot_message = event['add_time_slot_message']
        # Send message to WebSocket
        await self.send_json({
            "add_time_slot_message": add_time_slot_message
        })

    async def add_time_slot(self, user_id, data):

        print(" DOCTOR PROFILE: add_time_slot")
        #is_auth = is_authenticated(self.user)
        try:
            time_slots = await add_time_slot_or_error(user_id, data)
            self.doctor_time_slots = json.loads(time_slots)
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
def add_time_slot_or_error(user_id, data):
    slot_date = data["slot_date"]
    slot_time = data["appointment_time"]

    print(slot_date)
    print(slot_time)

    try:
        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(user=user)

        new_slot_date = AppointmentSlot.objects.create(slot_date=slot_date)
        new_slot_date.save()

        for time in slot_time:
            #print(time["time"])
            new_slot_time = TimeSlot.objects.create(appointment_slot=new_slot_date, time=time['time'])
            new_slot_time.save()
            new_slot_date.save()
        doctor.available_slot.add(new_slot_date)


        all_slots = doctor.available_slot.all()

        serializers = ListAppointmentSlotSerializer(all_slots, many=True)

        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except AppointmentSlot.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

