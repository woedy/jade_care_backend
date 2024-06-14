from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from communications.models import PrivateChatRoom
from notifications.models import Notification
from user_profile.models import Doctor

User = settings.AUTH_USER_MODEL


APPOINTMENT_TYPE_CHOICES = (
    ('Covid', 'Covid'),
    ('New Problem', 'New Problem'),
    ('Problem Follow-up', 'Problem Follow-up'),
)


APPOINTMENT_MEDIUM_CHOICES = (
    ('Video Call', 'Video Call'),
    ('Voice Call', 'Voice Call'),
    ('Text Message', 'Text Message'),
    ('Walk in', 'Walk in'),

)



APPOINTMENT_PAYMENT_METHOD_CHOICES = (
    ('Momo', 'Momo'),
    ('Paypal', 'Paypal'),
    ('Bank', 'Bank'),
)


STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('Review', 'Review'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)




class AppointmentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (
                    Q(patient__last_name__icontains=query) |
                    Q(patient__first_name__icontains=query) |
                    Q(status__icontains=query ) |
                    Q(appointment_type__icontains=query) |
                    Q(appointment_medium__icontains=query) |
                    Q(doctor__user__last_name__icontains=query)

            )

            qs = qs.filter(or_lookup).distinct()
        return qs


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_patient")
    appointment_type = models.CharField(max_length=255, null=True, blank=True, choices=APPOINTMENT_TYPE_CHOICES)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointment_doctor")
    appointment_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    appointment_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    for_self = models.BooleanField(default=True)
    re_scheduled = models.BooleanField(default=True)
    appointment_medium = models.CharField(max_length=255, null=True, blank=True, choices=APPOINTMENT_MEDIUM_CHOICES)
    amount_to_pay = models.CharField(null=True, blank=True, max_length=100)
    payment_method = models.CharField(max_length=255, null=True, blank=True, choices=APPOINTMENT_PAYMENT_METHOD_CHOICES)
    review = models.TextField(null=True, blank=True)
    chat_room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="appointment_room", null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS_CHOICE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()


def post_save_appointment_room_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = PrivateChatRoom.objects.create(user1=instance.patient, user2=instance.doctor.user)
        instance.chat_room = obj
        instance.save()

post_save.connect(post_save_appointment_room_create_receiver, sender=Appointment)

def post_save_appointment_notification_receiver(sender, instance, created, *args, **kwargs):
    doctor_name = instance.doctor.user.last_name + " " + instance.doctor.user.first_name
    patient_name = instance.patient.last_name + " " + instance.patient.first_name

    pat_verb_text = "You booked an appointment with Dr. " + doctor_name + " for " + str(instance.appointment_date) + " - " + str(instance.appointment_time)
    doc_verb_text = patient_name + " has booked an appointment with you on " + str(instance.appointment_date) + " - " + str(instance.appointment_time)

    appointment_ct = ContentType.objects.get_for_model(Appointment)

    if created:
        notification = Notification.objects.create(
            patient=instance.patient,
            doctor=instance.doctor.user,
            subject="New Appointment",
            pat_verb=pat_verb_text,
            doc_verb=doc_verb_text,
            content_type=appointment_ct,
            object_id=instance.id,
        )
        notification.save()


post_save.connect(post_save_appointment_notification_receiver, sender=Appointment)


class AppointmentForOther(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="appointment_for_other")
    last_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="appointment_payment")
    last_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(null=True, blank=True, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AppointmentMedium(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)


class TransferDoctor(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointment_transfer')
    new_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='new_doctor')
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

