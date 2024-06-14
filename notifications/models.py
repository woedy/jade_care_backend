from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_not")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="doctor_not")

    redirect_url = models.URLField(max_length=500, null=True, unique=False, blank=True, help_text="The URL to be visited when a notification is clicked.")

    subject = models.CharField(max_length=500, unique=False, blank=True, null=True)
    pat_verb = models.CharField(max_length=500, unique=False, blank=True, null=True)
    doc_verb = models.CharField(max_length=500, unique=False, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    pat_read = models.BooleanField(default=False)
    doc_read = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.pat_verb

    def get_content_object_type(self):
        return str(self.content_object.get_cname)