from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment, AppointmentForOther, Payment
from user_profile.models import Doctor, PersonalInfo

User = get_user_model()

class PersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo']



class AppointmentUserSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info']



class AppointmentDoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ['id', 'title', 'rating', 'available_slot']


class AppointmentForOtherSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentForOther
        fields = ['id', 'last_name', 'first_name', 'email', 'phone']


class AppointmentPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'last_name', 'first_name', 'email', 'phone', 'amount']


class ListUserAppointmentSerializer(serializers.ModelSerializer):
    patient = AppointmentUserSerializer()
    doctor = AppointmentDoctorSerializer()
    appointment_for_other = AppointmentForOtherSerializer()
    appointment_payment = AppointmentPaymentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_type', 'doctor', 'appointment_date', 'appointment_time', 'reason', 'for_self', 'appointment_for_other', 'appointment_medium', 'amount_to_pay', 'appointment_payment', 'payment_method', 'review', 'chat_room',  'status']






class DetailDoctorAppointmentSerializer(serializers.ModelSerializer):
    patient = AppointmentUserSerializer()
    appointment_for_other = AppointmentForOtherSerializer()
    appointment_payment = AppointmentPaymentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_type', 'doctor', 'appointment_date', 'appointment_time', 'reason', 'for_self', 'appointment_for_other', 'appointment_medium', 'amount_to_pay', 'appointment_payment', 'payment_method', 'review', 'chat_room', 'status', 'patient_prescriptions']

