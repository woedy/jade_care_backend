from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_profile.models import Doctor, Patient

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    #personal_info = PersonalInfoSerializer()
    #user_social_medias = SocialMediaSerializer(many=True)
    #user_schools = SchoolSerializer(many=True)
    #user_addresses = AddressSerializer(many=True)
    #user_emergency_contacts = EmergencyContactSerializer(many=True)
    #user_languages = UserLanguageSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name', 'personal_info', 'user_social_medias', 'user_addresses', 'user_emergency_contacts', 'user_languages']


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.is_active = True
        user.is_patient = True
        user.save()
        return user



class DocRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.is_active = True
        user.is_doctor = True
        user.save()

        doctor = Doctor.objects.create(
            user=user
        )
        doctor.save()
        return user



class AdminRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.is_active = True
        user.admin = True
        user.is_doctor = True
        user.save()

        doctor = Doctor.objects.create(
            user=user
        )
        doctor.save()
        return user