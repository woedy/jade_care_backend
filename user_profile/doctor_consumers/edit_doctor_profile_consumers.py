import base64
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from appointments.api.serializers.serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from user_profile.doctor_serializers.doctor_profile_serializer import DoctorProfileSerializer
from user_profile.models import PersonalInfo, Patient, Doctor
from user_profile.patient_serializers.patient_profile_serializer import PatientProfileSerializer

User = get_user_model()

class EditDoctorProfileConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.doctor_profile = None


        await self.accept()

    async def receive_json(self, content):
        print("EditDoctorProfileConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "edit_doctor_profile":
                print("CONTENT: Command: " + str(command))
                #print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'edit_doctor_profile_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.edit_doctor_profile(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'edit_doctor_profile_message',
                        'edit_doctor_profile_message': self.doctor_profile
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND DOCTOR MESSAGE
    ####################

    async def edit_doctor_profile_message(self, event):
        edit_doctor_profile_message = event['edit_doctor_profile_message']
        # Send message to WebSocket
        await self.send_json({
            "edit_doctor_profile_message": edit_doctor_profile_message
        })

    async def edit_doctor_profile(self, user_id, data):

        print("DOCTOR PROFILE: edit_doctor_profile")
        #is_auth = is_authenticated(self.user)
        try:
            profile = await edit_doctor_profile_or_error(user_id, data)
            self.patient_profile = json.loads(profile)
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
def edit_doctor_profile_or_error(user_id, data):


    username = data["username"]
    email = data["email"]
    last_name = data["last_name"]
    first_name = data["first_name"]

    photo = data["personal_info"]['photo']
    country = data["personal_info"]['country']
    gender = data["personal_info"]['gender']
    dob = data["personal_info"]['dob']
    marital_status = data["personal_info"]['marital_status']
    phone = data["personal_info"]['phone']

    title = data["doctor"]['title']

    try:
        user = User.objects.get(id=user_id)
        personal_info = PersonalInfo.objects.get(user=user)
        doctor = Doctor.objects.get(user=user)

        # USER info
        if username != None:
            user.username = username
            user.save()

        if email != None:
            user.email = email
            user.save()

        if last_name != None:
            user.last_name = last_name
            user.save()

        if first_name != None:
            user.first_name = first_name
            user.save()

        # Personal info
        if photo != None:
            personal_info.photo = base64_file(photo)
            personal_info.save()
            user.save()


        if country != None:
            personal_info.country = country
            personal_info.save()
            user.save()


        if gender != None:
            personal_info.gender = gender
            personal_info.save()
            user.save()

        if dob != None:
            personal_info.dob = dob
            personal_info.save()
            user.save()

        if marital_status != None:
            personal_info.marital_status = marital_status
            personal_info.save()
            user.save()

        if phone != None:
            personal_info.phone = phone
            personal_info.save()
            user.save()

        # PATIENT info

        if title != None:
            doctor.title = title
            doctor.save()
            user.save()



        serializers = DoctorProfileSerializer(user, many=False)
        if serializers:
            data = serializers.data
            #print(json.dumps(data))
            return json.dumps(data)
    except User.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


def base64_file(data, name="File_name", ext=".jpg"):
    print("############## DAAATAAAAAA")
    file = ContentFile(base64.b64decode(data), name=name+ext)
    return file
