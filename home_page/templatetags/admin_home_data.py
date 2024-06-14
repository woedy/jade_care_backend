from datetime import date, timedelta

from django import template

from appointments.models import Appointment
from home_page.api.doc_home_serializers import ListDocAppointmentHomeSerializer
from notifications.api.serializers import ListDocNotificationSerializer
from notifications.models import Notification
from posts.models import Post
from recent_activities.models import RecentActivity
from user_profile.models import Doctor, Patient

register = template.Library()


@register.simple_tag
def get_admin_notification_count(user_id):

    notification = Notification.objects.filter(doctor=user_id).filter(doc_read=False).order_by('-timestamp')
    notification_count = notification.count()

    return notification_count


@register.simple_tag
def get_admin_new_appointment_count():

    appointments = Appointment.objects.all()
    appointments_count = appointments.count()

    return appointments_count

@register.simple_tag
def get_this_month_appointment_count():

    appointments = Appointment.objects.all()
    appointments_count = appointments.count()

    return appointments_count

@register.simple_tag
def get_all_patient_count():

    patients = Patient.objects.all()
    patients_count = patients.count()

    return patients_count


@register.inclusion_tag("home_page/recent_activities.html")
def get_recent_activities(user_id):
    context = {}

    recent_activities = RecentActivity.objects.filter(user=user_id).order_by('-timestamp')[:5]
    context["recent_activities"] = recent_activities

    return context




@register.inclusion_tag("base/notification_snippet_doc.html")
def get_recent_notification_admin(user_id):
    context = {}



    notifications_data = []
    notifications = Notification.objects.filter(doctor=user_id).order_by('-id')[:3]


    context["notifications_data"] = notifications
    context["notifications_count"] = notifications.count()

    return context



@register.inclusion_tag("base/admin/all_appointment_snippet.html")
def get_recent_appointments():
    context = {}

    appointments_data = []
    doc_appointments = Appointment.objects.all().order_by('-id')[:5]
    appointments_data = doc_appointments

    context["appointments_data"] = appointments_data

    return context


@register.inclusion_tag("base/admin/all_patients_snippet.html")
def get_all_patients():
    context = {}

    all_patient_data = []
    all_patient = Patient.objects.all().order_by('-id')[:5]
    all_patient_data = all_patient

    context["all_patient_data"] = all_patient_data

    return context



@register.inclusion_tag("base/admin/recent_news_snippet.html")
def get_recent_news():
    context = {}

    all_posts_data = []
    all_post = Post.objects.all().order_by('-id')[:5]
    all_posts_data = all_post

    context["all_posts_data"] = all_posts_data

    return context
