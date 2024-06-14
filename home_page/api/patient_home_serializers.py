from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment, AppointmentForOther, Payment
from user_profile.models import Doctor, PersonalInfo

User = get_user_model()



class HomePersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo', 'phone']


class HomeUserSerializer(serializers.ModelSerializer):
    personal_info = HomePersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info']


class DoctorsSerializer(serializers.ModelSerializer):
    user = HomeUserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'rating', 'title', 'available_slot']



class ListUserAppointmentHomeSerializer(serializers.ModelSerializer):
    doctor = DoctorsSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'appointment_type', 'doctor', 'appointment_date', 'appointment_time', 'reason', 'for_self', 'appointment_for_other', 'appointment_medium', 'amount_to_pay', 'appointment_payment', 'payment_method', 'review', 'status']




