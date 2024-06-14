from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment, AppointmentForOther, Payment, AppointmentMedium
from user_profile.models import Doctor

User = get_user_model()



class AppointmentMediumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentMedium
        fields = ['id', 'name', 'price']


