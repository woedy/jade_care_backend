
from django.urls import path, include

from user_profile.views import patient_profile_page, list_all_doctors_ajax, doctor_profile_page, add_timeslot_doc, \
    view_timeslot_doc, admin_profile_page, list_all_doctors_admin, doctor_detail_admin, \
    list_all_patients_admin, patient_detail_admin, list_all_doctors_schedule_admin

app_name = "user_profile"

urlpatterns = [
    path("patient_profile/", patient_profile_page, name="patient_profile"),
    # path('patient_profile/<user_id>/edit/cropImage/', crop_image, name="crop_image"),
    path("doctor_profile/", doctor_profile_page, name="doctor_profile"),
    path("admin_profile/", admin_profile_page, name="admin_profile"),
    #path("doctor_profile/", DoctorProfileView.as_view(), name="doctor_profile"),
    path("list_all_doctors_ajax/", list_all_doctors_ajax, name="list_all_doctors_ajax"),

    path("add_timeslot_doc/", add_timeslot_doc, name="add_timeslot_doc"),
    path("view_timeslot_doc/", view_timeslot_doc, name="view_timeslot_doc"),


    path("list_all_doctors_admin/", list_all_doctors_admin, name="list_all_doctors_admin"),
    path("doctor_detail_admin/<id>/", doctor_detail_admin, name="doctor_detail_admin"),

    path("list_all_patients_admin/", list_all_patients_admin, name="list_all_patients_admin"),
    path("patient_detail_admin/<id>/", patient_detail_admin, name="patient_detail_admin"),

    path("list_all_doctors_schedule_admin/", list_all_doctors_schedule_admin, name="list_all_doctors_schedule_admin"),

]
