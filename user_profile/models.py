import os
import random

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



def upload_ghanacard_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "ghana_card/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_default_profile_image():
    return "defaults/default_profile_image.png"


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)

SOCIAL_MEDIA_CHOICES = (
    ('Facebook', 'Facebook'),
    ('Twitter', 'Twitter'),
    ('Youtube', 'Youtube'),
    ('Instagram', 'Instagram'),
    ('Whatsapp', 'Whatsapp'),
    ('TikTok', 'TikTok'),
    ('LinkedIn', 'LinkedIn'),
    ('Viber', 'Viber'),
    ('Snapchat', 'Snapchat'),
    ('Telegram', 'Telegram'),

)


class SocialMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_social_medias')
    name = models.CharField(max_length=255, null=True, blank=True, choices=SOCIAL_MEDIA_CHOICES)
    link = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    country = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_image_path, null=True, blank=True, default=get_default_profile_image)
    ghana_card = models.ImageField(upload_to=upload_ghanacard_path, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    marital_status = models.BooleanField(default=False)
    profile_complete = models.BooleanField(default=False)
    phone = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def post_save_user_personal_info(sender, instance, *args, **kwargs):
    if not instance.photo:
        instance.photo = get_default_profile_image()


post_save.connect(post_save_user_personal_info, sender=PersonalInfo)


class AppointmentSlot(models.Model):
    slot_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TimeSlot(models.Model):
    appointment_slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="appointment_time")
    time = models.TimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DoctorManager(BaseUserManager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(about__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__first_name__icontains=query)


            )

            qs = qs.filter(or_lookup).distinct()
        return qs


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    available_slot = models.ManyToManyField(AppointmentSlot, blank=True, related_name="user_appointment_slots")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return f"/user_profile/doctor_detail_admin/{self.id}/"

    objects = DoctorManager()



class PatientManager(BaseUserManager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (
                    Q(user__last_name__icontains=query) |
                    Q(user__first_name__icontains=query)

            )

            qs = qs.filter(or_lookup).distinct()
        return qs




class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    blood_pressure = models.CharField(max_length=200, null=True, blank=True)
    blood_sugar = models.CharField(max_length=200, null=True, blank=True)
    temperature = models.CharField(max_length=200, null=True, blank=True)
    heart_rate = models.CharField(max_length=200, null=True, blank=True)
    bmi = models.CharField(max_length=200, null=True, blank=True)
    respiratory_rate = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    objects = PatientManager()

    def get_absolute_url(self):
        return f"/user_profile/patient_detail_admin/{self.id}/"


class Allergy(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='patient_allergies')
    allergy = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    allergen = models.CharField(max_length=200, null=True, blank=True)
    reaction = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.allergy


class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_diagnosis')
    type = models.IntegerField(null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type




class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


RELATIONSHIP_CHOICES = (
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sibling', 'Sibling'),
)


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_emergency_contacts')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    relationship = models.CharField(choices=RELATIONSHIP_CHOICES, max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_education')
    name_of_school = models.CharField(max_length=255, null=True, blank=True)
    program = models.CharField(max_length=255, null=True, blank=True)
    from_date = models.DateTimeField(null=True, blank=True)
    to_date = models.DateTimeField(null=True, blank=True)


    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_experience')
    experience = models.CharField(max_length=255, null=True, blank=True)
    since = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_languages')
    language = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email + " - " + self.language
