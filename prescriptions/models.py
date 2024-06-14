from django.conf import settings
from django.db import models

from appointments.models import Appointment

User = settings.AUTH_USER_MODEL

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="patient_prescriptions")
    medication_name = models.CharField(max_length=400, null=True, blank=True)
    generic_name = models.CharField(max_length=400, null=True, blank=True)
    dosage = models.CharField(max_length=400, null=True, blank=True)
    frequency = models.CharField(max_length=400, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presc_patient")



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
