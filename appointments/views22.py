from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from appointments.api.serializers.appointment_detail_serializers import AppointmentDetailSerializer
from appointments.models import Appointment
from user_profile.models import Doctor

User = get_user_model()

@csrf_exempt
def make_appointment_page(request):
    context = {}

    if request.method == "POST":
        appointment_type = request.POST['appointment_type']
        doctor_id = request.POST['doctor']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        reason = request.POST['reason']
        for_self = request.POST['for_self']

        other_data_last_name = request.POST['other_data[last_name]']
        other_data_first_name = request.POST['other_data[first_name]']
        other_data_email = request.POST['other_data[email]']
        other_data_phone = request.POST['other_data[phone]']

        appointment_medium = request.POST['appointment_medium']
        appointment_price = request.POST['appointment_price']
        payment_type = request.POST['payment_type']


        payment_data_last_name = request.POST['payment_data[last_name]']
        payment_data_first_name = request.POST['payment_data[first_name]']
        payment_data_email = request.POST['payment_data[email]']
        payment_data_phone = request.POST['payment_data[phone]']

        patient = get_object_or_404(User, id=request.user.id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        new_appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_type=appointment_type,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            for_self=for_self,
            appointment_medium=appointment_medium,
            amount_to_pay=appointment_price,
            payment_method=payment_type,

        )

        new_appointment.save()

        print(appointment_type)
        print(doctor_id)
        print(appointment_date)
        print(appointment_time)
        print(reason)
        print(for_self)

        print(other_data_last_name)
        print(other_data_first_name)
        print(other_data_email)
        print(other_data_phone)

    return render(request, 'appointments/make_appointment.html', context)




def appointment_detail_page_doc(request, id):

    print(id)

    context = {}
    appointment_detail = get_object_or_404(Appointment, id=id)
    serializers = AppointmentDetailSerializer(appointment_detail, many=False)

    if serializers:
        data = serializers.data
        context['appointment_detail'] = data

    return render(request, 'appointments/appointment_detail_doc.html', context)




def appointment_detail_page_pat(request, id):

    print(id)

    context = {}
    appointment_detail = get_object_or_404(Appointment, id=id)
    serializers = AppointmentDetailSerializer(appointment_detail, many=False)

    if serializers:
        data = serializers.data
        context['appointment_detail'] = data

    return render(request, 'appointments/appointment_detail_pat.html', context)

def contact_patient_page(request):

    print(id)

    context = {}


    return render(request, 'appointments/contact_patient.html', context)



def make_appointment_ajax(request):
    context = {}

    appointment_type = request.GET.get('appointment_type', None)
    print(appointment_type)

    data = {}
    data['appointment_type'] = "WOOOOOOOOO"

    return JsonResponse(data)
