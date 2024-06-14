from django.contrib.auth import get_user_model
from rest_framework import serializers

from notifications.models import Notification
from user_profile.models import Doctor, PersonalInfo

User = get_user_model()


class PersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo']

class DocUserSerializer(serializers.ModelSerializer):

    personal_info = PersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'personal_info']




class ListNotificationSerializer(serializers.ModelSerializer):

    doctor = DocUserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'patient', 'doctor', 'redirect_url', 'subject', 'doc_verb', 'pat_verb', 'timestamp', 'pat_read', 'content_type', 'object_id']



class PatientUserSerializer(serializers.ModelSerializer):

    personal_info = PersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'personal_info']





class ListDocNotificationSerializer(serializers.ModelSerializer):

    patient = PatientUserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'patient', 'doctor', 'redirect_url', 'subject', 'doc_verb', 'pat_verb', 'timestamp', 'doc_read', 'content_type', 'object_id']



class ListPatNotificationSerializer(serializers.ModelSerializer):

    patient = PatientUserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'patient', 'doctor', 'redirect_url', 'subject', 'doc_verb', 'pat_verb', 'timestamp', 'doc_read', 'content_type', 'object_id']

