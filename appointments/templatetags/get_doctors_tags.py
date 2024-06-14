from django import template

from appointments.models import AppointmentMedium
from user_profile.models import Doctor

register = template.Library()

@register.simple_tag
def get_doctors():
    return Doctor.objects.all().count()


@register.inclusion_tag("appointments/all_doctors.html")
def get_all_doctors():
    context = {}

    all_doctors = Doctor.objects.all()
    context["all_doctors"] = all_doctors

    return context



@register.inclusion_tag("appointments/doctor_detail.html")
def get_doctor_detail(id):
    context = {}

    doctor_detail = Doctor.objects.get(id=id)
    context["doctor"] = doctor_detail

    return context


@register.inclusion_tag("appointments/appointment_mediums.html")
def get_appointment_mediums():
    context = {}

    appointment_mediums = AppointmentMedium.objects.all()
    context["appointment_mediums"] = appointment_mediums

    return context
