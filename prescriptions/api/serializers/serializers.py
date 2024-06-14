from django.contrib.auth import get_user_model
from rest_framework import serializers

from prescriptions.models import Prescription

User = get_user_model()


class ListPrescriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'medication_name', 'generic_name', 'dosage', 'frequency', 'instructions', 'patient']






