from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_profile.models import PersonalInfo, Patient, SocialMedia, Address, EmergencyContact, UserLanguage, Doctor, \
    AppointmentSlot, TimeSlot

User = get_user_model()


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ['id', 'country', 'gender', 'photo', 'dob', 'marital_status', 'phone']




class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'rating', 'title']


class DoctorUserSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info', 'user_social_medias',
                  'user_addresses', 'user_emergency_contacts', 'user_languages', 'doctor']



class DetailDoctorUserSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info', 'doctor']



class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'appointment_slot', 'time']


class AppointmentSlotSerializer(serializers.ModelSerializer):
    appointment_time = TimeSlotSerializer(many=True)

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'slot_date', 'appointment_time']




class DetailDoctorsSerializer(serializers.ModelSerializer):
    user = DetailDoctorUserSerializer()
    available_slot = AppointmentSlotSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'rating', 'title', 'available_slot']

