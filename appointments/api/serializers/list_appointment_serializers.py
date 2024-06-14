from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment
from user_profile.models import Doctor, PersonalInfo

User = get_user_model()

class AppointmentPersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo']

class AppointmentUserSerializer(serializers.ModelSerializer):
    personal_info = AppointmentPersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info']


class AppointmentDoctorSerializer(serializers.ModelSerializer):
    user = AppointmentUserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'title', 'rating', 'available_slot', 'user']


class ListUserAppointmentSerializer(serializers.ModelSerializer):
    doctor = AppointmentDoctorSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_type', 'doctor', 'appointment_date', 'appointment_time', 'reason', 'for_self', 'appointment_for_other', 'appointment_medium', 'amount_to_pay', 'appointment_payment', 'payment_method', 'review', 'chat_room', 'status']



