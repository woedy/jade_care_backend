import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from appointments.api.serializers.serializers import ListUserAppointmentSerializer
from appointments.models import Appointment, AppointmentForOther, Payment
from communications.models import PrivateChatRoom
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from notifications.models import Notification
from recent_activities.models import RecentActivity
from user_profile.models import Doctor, Patient

User = get_user_model()

class AddAppointmentConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.user_appointments = None


        await self.accept()

    async def receive_json(self, content):
        print("AddAppointmentConsumer: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "add_appointment":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'add_appointment_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.add_user_appointment(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'add_appointment_message',
                        'add_appointment_message': self.user_appointments
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND APPOINTMENT MESSAGE
    ####################

    async def add_appointment_message(self, event):
        add_appointment_message = event['add_appointment_message']
        # Send message to WebSocket
        await self.send_json({
            "add_appointment_message": add_appointment_message
        })

    async def add_user_appointment(self, user_id, data):

        print(" PROJECT DETAIL: get_project_detail")
        #is_auth = is_authenticated(self.user)
        try:
            appointments = await add_user_appointment_or_error(user_id, data)
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
def add_user_appointment_or_error222(user_id, data):
    print("##############################################")
    print("##############################################")
    print("##############################################")


    #patient_id = data["patient"]['id']
    appointment_type = data["appointment_type"]
    doctor_id = data["doctor"]

    appointment_date = data["appointment_date"]
    appointment_time = data["appointment_time"]
    reason = data["reason"]
    for_self = data["for_self"]

    appointment_for_other = data["appointment_for_other"]
    appointment_medium = data["appointment_medium"]
    amount_to_pay = data["amount_to_pay"]
    appointment_payment = data["appointment_payment"]
    payment_method = data["payment_method"]
    review = data["review"]

    user = User.objects.get(id=user_id)
    patient = Patient.objects.get(user=user)
    doctor = Doctor.objects.get(id=doctor_id)


    print(patient)
    print(appointment_type)
    print(doctor_id)

    print(appointment_date)
    print(appointment_time)
    print(reason)

    print(for_self)
    print(appointment_for_other)
    print(appointment_medium)

    print(amount_to_pay)
    print(appointment_payment)
    print(payment_method)
    print(review)

    print("##############################################")
    print("##############################################")
    print("##############################################")

    try:
        new_appointment = Appointment.objects.create(
            patient=patient,
        )
        new_appointment.save()

        user_appointments = Appointment.objects.filter(patient=user_id).order_by('-id')
        serializers = ListUserAppointmentSerializer(user_appointments, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")



@database_sync_to_async
def add_user_appointment_or_error(user_id, data):
    print("##############################################")
    print("##############################################")
    print("##############################################")


    #patient_id = data["patient"]['id']
    appointment_type = data["appointment_type"]
    doctor_id = data["doctor"]

    appointment_date = data["appointment_date"]
    appointment_time = data["appointment_time"]
    reason = data["reason"]
    for_self = data["for_self"]


    appointment_medium = data["appointment_medium"]
    amount_to_pay = data["amount_to_pay"]
    appointment_payment = data["appointment_payment"]
    payment_method = data["payment_method"]
    review = data["review"]

    user = User.objects.get(id=user_id)
    patient = Patient.objects.get(user=user)
    doctor = Doctor.objects.get(id=doctor_id)


    #print(patient_id)
    print(appointment_type)
    print(doctor_id)

    print(appointment_date)
    print(appointment_time)
    print(reason)

    print(for_self)
    print(appointment_medium)

    print(amount_to_pay)
    print(appointment_payment)
    print(payment_method)
    print(review)

    print("##############################################")
    print("##############################################")
    print("##############################################")

    try:
        new_appointment = Appointment.objects.create(
            patient=user,
            appointment_type=appointment_type,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            for_self=for_self,
            appointment_medium=appointment_medium,
            amount_to_pay=amount_to_pay,
            payment_method=payment_method,
            review=review,
            status="Pending"
        )

        appointment_for_other = data["appointment_for_other"]

        appointment_for_other = AppointmentForOther.objects.create(
            appointment=new_appointment,
            last_name=appointment_for_other['last_name'],
            first_name=appointment_for_other['first_name'],
            email=appointment_for_other['email'],
            phone=appointment_for_other['phone'],
        )
        appointment_for_other.save()

        new_payment = Payment.objects.create(
            appointment=new_appointment,
            last_name=appointment_payment['last_name'],
            first_name=appointment_payment['first_name'],
            email=appointment_payment['email'],
            phone=appointment_payment['phone'],
            amount=appointment_payment['amount'],
        )
        new_payment.save()
        new_appointment.save()

        doctor_name = doctor.user.last_name + " " + doctor.user.first_name
        patient_name = patient.user.last_name + " " + patient.user.first_name

        pat_verb_text = "You booked an appointment with " + doctor_name + " on " + appointment_date + " - " + appointment_time
        doc_verb_text = patient_name + " has booked an appointment with you on " + appointment_date + " - " + appointment_time

        #appointment_ct = ContentType.objects.get_for_model(Appointment)
        #new_notification = Notification.objects.create(
        #    patient=user,
        #    doctor=doctor.user,
        #    subject="New Appointment",
        #    pat_verb=pat_verb_text,
        #    doc_verb=doc_verb_text,
        #    content_type=appointment_ct,
        #    object_id=new_appointment.id,
        #)
        #new_notification.save()

        RecentActivity.objects.create(
            user=user,
            subject="New Appointment - Mobile",
            verb="You created a new appointment on mobile"
        )

        user_appointments = Appointment.objects.filter(patient=user_id).order_by('-id')
        serializers = ListUserAppointmentSerializer(user_appointments, many=True)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Appointment.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

