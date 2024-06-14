from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment, AppointmentForOther, Payment
from user_profile.models import Doctor, PersonalInfo, Patient

User = get_user_model()



class HomePersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo', 'phone']


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id', 'height', 'weight', 'blood_group']



class HomeUserSerializer(serializers.ModelSerializer):
    personal_info = HomePersonalInfoSerializer()
    patient = PatientSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info', "patient"]






class ListDocAppointmentHomeSerializer(serializers.ModelSerializer):
    patient = HomeUserSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_type', 'doctor', 'appointment_date', 'appointment_time', 'reason', 'for_self', 'appointment_for_other', 'appointment_medium', 'amount_to_pay', 'appointment_payment', 'payment_method', 'review', 'status']

