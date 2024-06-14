from django.db import models

from user_profile.models import Patient


INVOICE_STATUS = (
    ('Paid', 'Paid'),
    ('Pending', 'Pending'),
    ('Paid Partially', 'Paid Partially'),

)


class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_invoices')
    status = models.CharField(choices=INVOICE_STATUS, max_length=200, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField()

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
