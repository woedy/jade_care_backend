import base64
import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from user_profile.doctor_serializers.list_doc_serializer import ListDoctorsSerializer, DoctorUserSerializer
from user_profile.models import Doctor, PersonalInfo, Patient, AppointmentSlot, TimeSlot


User = get_user_model()

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"



def patient_profile_page(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    personal_info = get_object_or_404(PersonalInfo, user=user)
    patient = get_object_or_404(Patient, user=user)

    if request.method == "POST":
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']

        gender = request.POST['gender']
        phone = request.POST['phone']
        dob = request.POST['dob']
        marital_status = request.POST['marital_status']
        country = request.POST['country']

        height = request.POST['height']
        weight = request.POST['weight']
        blood_group = request.POST['blood_group']
        blood_pressure = request.POST['blood_pressure']
        blood_sugar = request.POST['blood_sugar']

        temperature = request.POST['temperature']
        heart_rate = request.POST['heart_rate']

        bmi = request.POST['bmi']
        respiratory_rate = request.POST['respiratory_rate']

        if email != None:
            user.email = email
            user.save()

        if last_name != None:
            user.last_name = last_name
            user.save()

        if first_name != None:
            user.first_name = first_name
            user.save()

        if gender != None:
            personal_info.gender = gender
            personal_info.save()
            user.save()

        if dob != None and dob != "":
            personal_info.dob = dob
            personal_info.save()
            user.save()

        if phone != None:
            personal_info.phone = phone
            personal_info.save()
            user.save()

        if country != None:
            personal_info.country = country
            personal_info.save()
            user.save()

        if marital_status == 'married':
            personal_info.marital_status = True
            personal_info.save()
            user.save()

        elif marital_status == 'single':
            personal_info.marital_status = False
            personal_info.save()
            user.save()


        if height != None:
            patient.height = height
            patient.save()
            user.save()

        if weight != None:
            patient.weight = weight
            patient.save()
            user.save()

        if blood_group != None:
            patient.blood_group = blood_group
            patient.save()
            user.save()

        if blood_pressure != None:
            patient.blood_pressure = blood_pressure
            patient.save()
            user.save()

        if blood_sugar != None:
            patient.blood_sugar = blood_sugar
            patient.save()
            user.save()

        if temperature != None:
            patient.temperature = temperature
            patient.save()
            user.save()

        if heart_rate != None:
            patient.heart_rate = heart_rate
            patient.save()
            user.save()

        if bmi != None:
            patient.bmi = bmi
            patient.save()
            user.save()

        if respiratory_rate != None:
            patient.respiratory_rate = respiratory_rate
            patient.save()
            user.save()



    context['user_profile'] = user

    return render(request, 'user_profile/patient_profile.html', context)

@csrf_exempt
# def crop_image(request, *args, **kwargs):
#     payload = {}
#     user = request.user
#     personal_info = get_object_or_404(PersonalInfo, user=user)
#
#     if request.POST:
#         try:
#             imageString = request.POST.get("image")
#             url = save_temp_profile_image_from_base64String(imageString, user)
#             img = cv2.imread(url)
#
#             cropX = int(float(str(request.POST.get("cropX"))))
#             cropY = int(float(str(request.POST.get("cropY"))))
#             cropWidth = int(float(str(request.POST.get("cropWidth"))))
#             cropHeight = int(float(str(request.POST.get("cropHeight"))))
#
#             if cropX < 0:
#                 cropX = 0
#             if cropY < 0:  # There is a bug with cropperjs. y can be negative.
#                 cropY = 0
#             crop_img = img[cropY:cropY + cropHeight, cropX:cropX + cropWidth]
#
#             cv2.imwrite(url, crop_img)
#
#             personal_info.photo.delete()
#             personal_info.photo.save("profile_image.png", files.File(open(url, 'rb')))
#             personal_info.save()
#             user.save()
#
#             payload['result'] = "success"
#             payload['cropped_profile_image'] = personal_info.photo.url
#
#             # delete temp file
#             os.remove(url)
#
#         except Exception as e:
#             print("exception: " + str(e))
#             payload['result'] = "error"
#             payload['exception'] = str(e)
#
#     return HttpResponse(json.dumps(payload), content_type="application/json")


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"

    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
            os.mkdir(settings.TEMP + "/" + str(user.pk))
        url = os.path.join(settings.TEMP + "/" + str(user.pk), TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print("exception: " + str(e))
        # workaround for an issue I found
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
    return None


def doctor_profile_page(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    personal_info = get_object_or_404(PersonalInfo, user=user)
    doctor = get_object_or_404(Doctor, user=user)

    if request.method == "POST":
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        title = request.POST['title']

        gender = request.POST['gender']
        phone = request.POST['phone']
        dob = request.POST['dob']
        marital_status = request.POST['marital_status']
        country = request.POST['country']

        if email != None:
            user.email = email
            user.save()

        if last_name != None:
            user.last_name = last_name
            user.save()

        if first_name != None:
            user.first_name = first_name
            user.save()

        if title != None:
            doctor.title = title
            doctor.save()
            user.save()

        if gender != None:
            personal_info.gender = gender
            personal_info.save()
            user.save()

        if country != None:
            personal_info.country = country
            personal_info.save()
            user.save()

        if dob != None and dob != "":
            personal_info.dob = dob
            personal_info.save()
            user.save()

        if phone != None:
            personal_info.phone = phone
            personal_info.save()
            user.save()

        if marital_status == 'married':
            personal_info.marital_status = True
            personal_info.save()
            user.save()

        elif marital_status == 'single':
            personal_info.marital_status = False
            personal_info.save()
            user.save()

    context['user_profile'] = user

    return render(request, 'user_profile/doctor_profile.html', context)

def admin_profile_page(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    personal_info = get_object_or_404(PersonalInfo, user=user)
    doctor = get_object_or_404(Doctor, user=user)

    if request.method == "POST":
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        title = request.POST['title']

        gender = request.POST['gender']
        phone = request.POST['phone']
        dob = request.POST['dob']
        marital_status = request.POST['marital_status']
        country = request.POST['country']

        if email != None:
            user.email = email
            user.save()

        if last_name != None:
            user.last_name = last_name
            user.save()

        if first_name != None:
            user.first_name = first_name
            user.save()

        if title != None:
            doctor.title = title
            doctor.save()
            user.save()

        if gender != None:
            personal_info.gender = gender
            personal_info.save()
            user.save()

        if country != None:
            personal_info.country = country
            personal_info.save()
            user.save()

        if dob != None and dob != "":
            personal_info.dob = dob
            personal_info.save()
            user.save()

        if phone != None:
            personal_info.phone = phone
            personal_info.save()
            user.save()

        if marital_status == 'married':
            personal_info.marital_status = True
            personal_info.save()
            user.save()

        elif marital_status == 'single':
            personal_info.marital_status = False
            personal_info.save()
            user.save()

    context['user_profile'] = user

    return render(request, 'user_profile/admin_profile.html', context)

def list_all_doctors_ajax(request):
    context = {}

    appointment_type = request.GET.get('appointment_type', None)
    print(appointment_type)

    doctors = Doctor.objects.all().order_by('id')
    serializers = ListDoctorsSerializer(doctors, many=True)
    if serializers:
        data = serializers.data
        print(data)
        context["all_doctors"] = data
        context["test"] = "WOOOOOO"

    return JsonResponse(context)


def add_timeslot_doc(request):
    context = {}

    user = get_object_or_404(User, id=request.user.id)
    doctor = get_object_or_404(Doctor, user=user)

    if request.method == "POST":
        print(request.POST)
        print(request.POST['date'])
        print(request.POST.getlist('time[]'))
        timee = request.POST.getlist('time[]')
        newtt = timee.pop()
        print("POP TIMEE   " + newtt)

        new_slot_date = AppointmentSlot.objects.create(slot_date=request.POST['date'])
        new_slot_date.save()

        for time in request.POST.getlist('time[]'):
            print(time)
            if time != "":
                new_slot_time = TimeSlot.objects.create(appointment_slot=new_slot_date, time=time)
                new_slot_time.save()

        doctor.available_slot.add(new_slot_date)

        return redirect('user_profile:view_timeslot_doc')

    return render(request, 'user_profile/add_timeslot_doc.html', context)


def view_timeslot_doc(request):
    context = {}

    user = get_object_or_404(User, id=request.user.id)
    personal_info = get_object_or_404(PersonalInfo, user=user)
    doctor = get_object_or_404(Doctor, user=user)
    available_slots = doctor.available_slot.all().order_by('-id')
    context['available_slots'] = available_slots

    return render(request, 'user_profile/view_timeslot_doc.html', context)


def list_all_doctors_admin(request):

    context = {}

    doctors = Doctor.objects.all().order_by('id')

    context['all_doctors'] = doctors

    return render(request, 'user_profile/list_all_doctors_admin.html', context)



def doctor_detail_admin(request, id):

    context = {}

    doctor = get_object_or_404(Doctor, id=id)

    context['doctor_detail'] = doctor

    return render(request, 'user_profile/doctor_detail_admin.html', context)


def list_all_patients_admin(request):

    context = {}

    patients = Patient.objects.all().order_by('id').order_by('-id')

    context['all_patients'] = patients

    return render(request, 'user_profile/list_all_patients_admin.html', context)




def patient_detail_admin(request, id):

    context = {}

    patient = get_object_or_404(Patient, id=id)

    context['patient_detail'] = patient

    return render(request, 'user_profile/patient_profile_admin.html', context)


def list_all_doctors_schedule_admin(request):

    context = {}

    all_schedules = AppointmentSlot.objects.all().order_by('id')

    context['all_schedules'] = all_schedules

    return render(request, 'user_profile/list_all_doctors_schedule_admin.html', context)

