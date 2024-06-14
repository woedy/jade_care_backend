import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from appointments.api.serializers.appointment_detail_serializers import AppointmentDetailSerializer
from appointments.models import Appointment, AppointmentForOther, Payment, AppointmentMedium
from home_page.api.doc_home_serializers import ListDocAppointmentHomeSerializer
from recent_activities.models import RecentActivity
from user_profile.models import Doctor



User = get_user_model()


@csrf_exempt
def all_appointments_page(request):

    context = {}

    doctor = Doctor.objects.get(user=request.user.id)
    appointments_data = []
    doc_appointments = Appointment.objects.filter(doctor=doctor).order_by('-id')
    serializers = ListDocAppointmentHomeSerializer(doc_appointments, many=True)
    appointment_seria = serializers.data
    appointments_data = appointment_seria

    context["appointments_data"] = appointments_data

    return render(request, 'appointments/all_appointments.html', context)


@csrf_exempt
def all_appointments_admin_page(request):

    context = {}


    appointments_data = []
    appointments_data = Appointment.objects.all().order_by('id')


    context["appointments_data"] = appointments_data

    return render(request, 'appointments/all_appointments_admin.html', context)



@csrf_exempt
def make_appointment_page(request):
    context = {}


    return render(request, 'appointments/make_appointment.html', context)

@csrf_exempt
def make_appointment_post(request):
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

        print(request.POST)

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
            status="Pending",
        )

        new_appointment.save()

        if for_self is False:
            appointment_for_other = AppointmentForOther.objects.create(
                appointment=new_appointment,
                last_name=other_data_last_name,
                first_name=other_data_first_name,
                email=other_data_email,
                phone=other_data_phone,
            )
            appointment_for_other.save()


        new_payment = Payment.objects.create(
            appointment=new_appointment,
            last_name=payment_data_last_name,
            first_name=payment_data_first_name,
            email=payment_data_email,
            phone=payment_data_phone,
            amount=appointment_price,
        )
        new_payment.save()

        RecentActivity.objects.create(
            user=patient,
            subject="New Appointment - Web",
            verb="You created a new appointment on the web"
        )
        return render(request, 'appointments/appointment_successful.html', context)

    return render(request, 'appointments/appointment_successful.html', context)


def appointment_successful_page(request):
    context = {}

    return render(request, 'appointments/appointment_successful.html', context)


def appointment_detail_page_doc(request, id):

    print(id)

    context = {}
    appointment_detail = get_object_or_404(Appointment, id=id)

    context['appointment_detail'] = appointment_detail

    return render(request, 'appointments/appointment_detail_doc.html', context)



def appointment_detail_page_admin(request, id):

    print(id)

    context = {}
    appointment_detail = get_object_or_404(Appointment, id=id)

    context['appointment_detail'] = appointment_detail

    return render(request, 'appointments/appointment_detail_admin.html', context)




def appointment_detail_page_pat(request, id):

    print(id)

    context = {}
    appointment_detail = get_object_or_404(Appointment, id=id)

    context['appointment_detail'] = appointment_detail

    return render(request, 'appointments/appointment_detail_pat.html', context)


@csrf_exempt
def withdraw_appointment_pat(request, id, *args, **kwargs):
    payload = {}
    user = request.user
    appointment = get_object_or_404(Appointment, id=id)

    if request.POST:
        try:
            action = request.POST.get("action")
            print(action)
            if action == "Withdraw Appointment":
                appointment.status = "Canceled"
                appointment.save()
                payload['result'] = "success"

                serializers = AppointmentDetailSerializer(appointment, many=False)

                if serializers:
                    data = serializers.data
                    payload['appointment_detail'] = data


        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")




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




def appointment_medium_page_admin(request):

    context = {}

    appointment_medium = AppointmentMedium.objects.all()

    context['mediums'] = appointment_medium


    return render(request, 'appointments/appointment_medium_admin.html', context)




def add_appointment_medium_page_admin(request):
    context = {}
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        print(name)
        print(price)
        AppointmentMedium.objects.create(
            name=name,
            price=price
        )

        return redirect('appointments:appointment_medium_page_admin')


    return render(request, 'appointments/add_appointment_medium_admin.html', context)


def appointment_video_call_page(request):
    context = {}



    return render(request, 'appointments/appointment_video_call.html', context)


def appointment_text_message_page(request, id):
    context = {}

    print(id)




    appointment = Appointment.objects.get(id=id)
    chat_room = appointment.chat_room

    user_1 = chat_room.user1
    user_2 = chat_room.user2

    if user_1 != request.user.id:
        print("Send user 1")
        context['other_user'] = user_2

    elif user_2 != request.user.id:
        print("Send user 2")
        context['other_user'] = user_1

    context['chat_room'] = chat_room




    return render(request, 'appointments/appointment_text_message.html', context)



def appointment_text_message_page_doc(request, id):
    context = {}

    print(id)


    appointment = Appointment.objects.get(id=id)
    chat_room = appointment.chat_room

    user_1 = chat_room.user1
    user_2 = chat_room.user2

    if user_1 != request.user.id:
        print("Send user 1")
        context['other_user'] = user_1

    elif user_2 != request.user.id:
        print("Send user 2")
        context['other_user'] = user_2

    context['chat_room'] = chat_room




    return render(request, 'appointments/appointment_text_message_doc.html', context)




@csrf_exempt
def approve_appointment_doc(request, id, *args, **kwargs):
    payload = {}
    user = request.user
    appointment = get_object_or_404(Appointment, id=id)

    if request.POST:
        try:
            action = request.POST.get("action")
            print(action)
            if action == "Approve Appointment":
                appointment.status = "Approved"
                appointment.save()
                payload['result'] = "success"

            if action == "Decline Appointment":
                appointment.status = "Declined"
                appointment.save()
                payload['result'] = "success"

            if action == "Start Appointment":
                appointment.status = "Started"
                appointment.save()
                payload['result'] = "success"

            if action == "Complete Appointment":
                appointment.status = "Completed"
                appointment.save()
                payload['result'] = "success"

            serializers = AppointmentDetailSerializer(appointment, many=False)

            if serializers:
                data = serializers.data
                payload['appointment_detail'] = data


        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")


