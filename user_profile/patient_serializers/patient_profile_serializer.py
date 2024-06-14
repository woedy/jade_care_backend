from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_profile.models import PersonalInfo, Patient, SocialMedia, Address, EmergencyContact, UserLanguage, Doctor, \
    AppointmentSlot, TimeSlot

User = get_user_model()


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ['id', 'user', 'country', 'gender', 'photo', 'dob', 'marital_status', 'phone']




class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'height', 'weight', 'blood_group', 'blood_pressure', 'blood_sugar', 'temperature', 'heart_rate', 'bmi','respiratory_rate' ]




class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'name', 'link']

class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = ['id', 'language']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line_1', 'address_line_2', 'country', 'region', 'city', 'town']




class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'full_name', 'relationship', 'email', 'phone',  'address_line_1', 'address_line_2', 'country', 'region', 'city', 'town']



class PatientProfileSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer()
    user_social_medias = SocialMediaSerializer(many=True)
    user_addresses = AddressSerializer(many=True)
    user_emergency_contacts = EmergencyContactSerializer(many=True)
    user_languages = UserLanguageSerializer(many=True)
    patient = PatientSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'personal_info', 'user_social_medias', 'user_addresses', 'user_emergency_contacts', 'user_languages', 'patient']






class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'appointment_slot', 'time']


class AppointmentSlotSerializer(serializers.ModelSerializer):
    appointment_time = TimeSlotSerializer(many=True)

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'slot_date', 'appointment_time']


