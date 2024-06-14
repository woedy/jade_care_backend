import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from appointments.api.serializers.appointment_detail_serializers import AppointmentDetailSerializer
from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from notifications.models import Notification
from user_profile.models import Patient, Doctor


User = get_user_model()

class ChangeAppointmentStateConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.appointment_state = None


        await self.accept()

    async def receive_json(self, content):
        print("ChangeAppointmentStateConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)
        appointment_id = content.get("appointment_id", None)
        appointment_state = content.get("appointment_state", None)

        try:
            if command == "change_appointment_state":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'change_state_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.change_appointment_state(user_id, data, appointment_id, appointment_state)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'change_appointment_state_message',
                        'change_appointment_state_message': self.appointment_state
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################

    async def change_appointment_state_message(self, event):
        change_appointment_state_message = event['change_appointment_state_message']
        # Send message to WebSocket
        await self.send_json({
            "change_appointment_state_message": change_appointment_state_message
        })

    async def change_appointment_state(self, user_id, data, appointment_id, appointment_state):

        print(" PROJECT DETAIL: change_appointment_state")
        #is_auth = is_authenticated(self.user)
        try:
            appointment_state = await change_appointment_state_or_error(user_id, data, appointment_id, appointment_state)
            self.appointment_state = json.loads(appointment_state)
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
def change_appointment_state_or_error(user_id, data, appointment_id, appointment_state):

    try:
        print("##############")
        print(appointment_state)
        appointment_detail = Appointment.objects.get(id=appointment_id)

        patient = appointment_detail.patient
        doctor = appointment_detail.doctor.user

        doctor_name = doctor.last_name + " " + doctor.first_name
        patient_name = patient.last_name + " " + patient.first_name


        appointment_date = appointment_detail.appointment_date
        appointment_time = appointment_detail.appointment_time

        appointment_ct = ContentType.objects.get_for_model(Appointment)

        appointment_detail.status = appointment_state
        appointment_detail.save(update_fields=['status'])


        if appointment_state == "Approved":
            pat_verb_text = "Dr. " + doctor_name + " approved your appointment for " + str(
                appointment_date) + " - " + str(appointment_time)
            doc_verb_text = "You approved " + patient_name + "'s appointment" + " for " + str(
                appointment_date) + " - " + str(appointment_time)
            new_notification = Notification.objects.create(
                patient=patient,
                doctor=doctor,
                subject="Appointment Approved",
                pat_verb=pat_verb_text,
                doc_verb=doc_verb_text,
                content_type=appointment_ct,
                object_id=appointment_detail.id,
            )
            new_notification.save()

        elif appointment_state == "Declined":
            pat_verb_text = "Dr. " + doctor_name + " declined your appointment for " + str(
                appointment_date) + " - " + str(appointment_time)
            doc_verb_text = "You declined " + patient_name + "'s appointment" + " for " + str(
                appointment_date) + " - " + str(appointment_time)
            new_notification = Notification.objects.create(
                patient=patient,
                doctor=doctor,
                subject="Appointment Declined",
                pat_verb=pat_verb_text,
                doc_verb=doc_verb_text,
                content_type=appointment_ct,
                object_id=appointment_detail.id,
            )
            new_notification.save()

        elif appointment_state == "Started":
            pat_verb_text = "Dr. " + doctor_name + " stated your appointment for " + str(
                appointment_date) + " - " + str(appointment_time)
            doc_verb_text = "You started " + patient_name + "'s appointment" + " for " + str(
                appointment_date) + " - " + str(appointment_time)
            new_notification = Notification.objects.create(
                patient=patient,
                doctor=doctor,
                subject="Appointment Started",
                pat_verb=pat_verb_text,
                doc_verb=doc_verb_text,
                content_type=appointment_ct,
                object_id=appointment_detail.id,
            )
            new_notification.save()

        elif appointment_state == "Completed":
            pat_verb_text = "Your appointment with Dr. " + doctor_name + " is over. "
            doc_verb_text = "You appointment with " + patient_name + " is over. "
            new_notification = Notification.objects.create(
                patient=patient,
                doctor=doctor,
                subject="Appointment Complete",
                pat_verb=pat_verb_text,
                doc_verb=doc_verb_text,
                content_type=appointment_ct,
                object_id=appointment_detail.id,
            )
            new_notification.save()


        serializers = AppointmentDetailSerializer(appointment_detail, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

