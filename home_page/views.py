from django.contrib.auth import get_user_model
from django.shortcuts import render

from appointments.models import Appointment
from home_page.api.patient_home_serializers import ListUserAppointmentHomeSerializer
from user_profile.models import PersonalInfo

User = get_user_model()


def home_page(request):
    context = {}

    return render(request, 'home_page/home_page.html', context)


def patient_home_page(request):
    context = {}


    user = User.objects.get(id=request.user.id)
    personal_info = PersonalInfo.objects.get(user=user)

    appointment_data = []
    user_appointments = Appointment.objects.filter(patient=request.user.id).order_by('-id')[:5]
    serializers = ListUserAppointmentHomeSerializer(user_appointments, many=True)
    appointment_seria = serializers.data
    appointment_data = appointment_seria

    context['appointment_data'] = appointment_data



    user_data = {}
    user_data["last_name"] = user.last_name
    user_data["first_name"] = user.first_name
    user_data['photo'] = personal_info.photo.url

    context['user_data'] = user_data

    return render(request, 'home_page/patient_home_page.html', context)


def doctor_home_page(request):
    context = {}

    return render(request, 'home_page/doctor_home_page.html', context)


def admin_home_page(request):
    context = {}

    return render(request, 'home_page/admin_home_page.html', context)