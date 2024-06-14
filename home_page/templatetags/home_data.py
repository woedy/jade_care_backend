from django import template

from appointments.models import Appointment
from home_page.api.doc_home_serializers import ListDocAppointmentHomeSerializer
from notifications.api.serializers import ListDocNotificationSerializer
from notifications.models import Notification
from recent_activities.models import RecentActivity
from user_profile.models import Doctor

register = template.Library()


@register.simple_tag
def get_home_data():

    return {"test": "WOOOOOOO"}


@register.simple_tag
def get_patient_notification_count(user_id):


    notification = Notification.objects.filter(patient=user_id).filter(pat_read=False).order_by('-timestamp')
    notification_count = notification.count()

    return notification_count

@register.simple_tag
def get_doctor_notification_count(user_id):

    notification = Notification.objects.filter(doctor=user_id).filter(doc_read=False).order_by('-timestamp')
    notification_count = notification.count()

    return notification_count


@register.inclusion_tag("home_page/recent_activities.html")
def get_recent_activities(user_id):
    context = {}

    recent_activities = RecentActivity.objects.filter(user=user_id).order_by('-timestamp')[:5]
    context["recent_activities"] = recent_activities

    return context




@register.inclusion_tag("home_page/recent_appointments_doc.html")
def get_recent_appointments_doc(user_id):
    context = {}

    doctor = Doctor.objects.get(user=user_id)

    appointments_data = []
    doc_appointments = Appointment.objects.filter(doctor=doctor).order_by('-id')[:3]
    serializers = ListDocAppointmentHomeSerializer(doc_appointments, many=True)
    appointment_seria = serializers.data
    appointments_data = appointment_seria

    context["appointments_data"] = appointments_data

    return context



@register.inclusion_tag("base/notification_snippet_doc.html")
def get_recent_notification_doc(user_id):
    context = {}



    notifications_data = []
    notifications = Notification.objects.filter(doctor=user_id).order_by('-id')[:3]


    context["notifications_data"] = notifications
    context["notifications_count"] = notifications.count()

    return context


@register.inclusion_tag("base/notification_snippet_pat.html")
def get_recent_notification_pat(user_id):
    context = {}



    notifications_data = []
    notifications = Notification.objects.filter(patient=user_id).order_by('-id')[:3]


    context["notifications_data"] = notifications
    context["notifications_count"] = notifications.count()

    return context
