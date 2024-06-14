
from django.urls import path, include

from appointments.views import make_appointment_page, make_appointment_ajax, \
    appointment_detail_page_doc, appointment_detail_page_pat, contact_patient_page, all_appointments_page, \
    appointment_successful_page, make_appointment_post, withdraw_appointment_pat, appointment_medium_page_admin, \
    add_appointment_medium_page_admin, appointment_video_call_page, appointment_text_message_page, \
    appointment_text_message_page_doc, approve_appointment_doc, all_appointments_admin_page, \
    appointment_detail_page_admin

app_name = "appointments"

urlpatterns = [
    path("all_appointments/", all_appointments_page, name="all_appointments"),
    path("all_appointments_admin/", all_appointments_admin_page, name="all_appointments_admin"),
    path("make_appointment/", make_appointment_page, name="make_appointment"),
    path("make_appointment_post/", make_appointment_post, name="make_appointment_post"),
    path("appointment_successful/", appointment_successful_page, name="appointment_successful"),
    path("appointment_detail_doc/<id>/", appointment_detail_page_doc, name="appointment_detail_doc"),
    path("appointment_detail_admin/<id>/", appointment_detail_page_admin, name="appointment_detail_admin"),

    path("appointment_detail_pat/<id>/", appointment_detail_page_pat, name="appointment_detail_pat"),
    path("withdraw_appointment_pat/<id>/", withdraw_appointment_pat, name="withdraw_appointment_pat"),
    path("contact_patient/", contact_patient_page, name="contact_patient"),

    path("make_appointment/", make_appointment_ajax, name="make_appointment_ajax"),

    path("appointment_medium_page_admin/", appointment_medium_page_admin, name="appointment_medium_page_admin"),
    path("add_appointment_medium_page_admin/", add_appointment_medium_page_admin, name="add_appointment_medium_page_admin"),

    path("appointment_video_call_page/", appointment_video_call_page,
         name="appointment_video_call_page"),
    path("appointment_text_message_page/<id>", appointment_text_message_page,
         name="appointment_text_message_page"),
    path("appointment_text_message_page_doc/<id>", appointment_text_message_page_doc,
         name="appointment_text_message_page_doc"),

    path("approve_appointment_doc/<id>/", approve_appointment_doc, name="approve_appointment_doc"),

]
