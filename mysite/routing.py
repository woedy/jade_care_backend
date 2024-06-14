from django.urls import path

from accounts.api.consumers.login_consumers import LoginConsumers
from appointments.api.consumers.add_appointment_consumers import AddAppointmentConsumer
from appointments.api.consumers.change_appointment_state_consumers import ChangeAppointmentStateConsumer
from appointments.api.consumers.get_appointment_consumers import GetAppointmentConsumer
from appointments.api.consumers.get_appointment_detail_consumers import GetAppointmentDetailConsumer
from appointments.api.consumers.get_appointment_medium_consumers import GetAppointmentMediumConsumers
from appointments.api.consumers.get_doc_appointment_consumers import GetDocAppointmentConsumer
from appointments.api.consumers.get_doc_appointment_details_consumers import GetDocAppointmentDetailsConsumer
from appointments.api.consumers.get_doctor_appointments_consumers import GetDoctorAppointmentsConsumer
from appointments.consumers.appointment_text_messages_consumers import AppointmentTextMessagePageConsumers
from communications.api.consumers.appointment_message_consumers import AppointmentMessageConsumers
from communications.api.consumers.chat_messages_admin_consumers import ChatMessagesAdminConsumers
from communications.api.consumers.chat_messages_doc_consumers import ChatMessagesDocConsumers
from communications.api.consumers.chat_messages_pat_consumers import ChatMessagesPatConsumers
from communications.video_call_consumers import WebVideoCallConsumers
from home_page.api.consumers.admin_home_consumers import GetAdminHomeDataConsumer
from home_page.api.consumers.doctor_home_consumers import GetDocHomeDataConsumer
from home_page.api.consumers.patient_home_consumers import GetPatientHomeDataConsumer
from notifications.api.doc_noti_consumers import DoctorNotificationConsumers
from notifications.api.pat_noti_consumers import PatientNotificationConsumers
from posts.api.consumers.add_article_consumers import AddArticleConsumers
from posts.api.consumers.edit_article_consumers import EditArticleConsumers
from posts.api.consumers.get_articles_consumers import GetAllArticlesConsumers
from prescriptions.api.consumers.add_prescription_consumers import AddPrescriptionsConsumer
from prescriptions.api.consumers.list_pat_prescriptions_consumers import ListPatPrescriptionsConsumer
from prescriptions.api.consumers.list_doc_prescriptions_consumers import ListDocPrescriptionsConsumer

from prescriptions.api.consumers.list_prescriptions_consumers import ListPrescriptionsConsumer
from search.api.search_consumers import SearchConsumers
from user_profile.doctor_consumers.add_time_slot_consumers import AddTimeSlotConsumers
from user_profile.doctor_consumers.doctor_detail_consumers import DoctorDetailConsumers
from user_profile.doctor_consumers.edit_doctor_profile_consumers import EditDoctorProfileConsumer
from user_profile.doctor_consumers.get_doctor_profile_consumers import GetDoctorProfileConsumer
from user_profile.patient_consumers.edit_patient_profile_consumers import EditPatientProfileConsumer
from user_profile.patient_consumers.get_patient_profile_consumers import GetPatientProfileConsumer
from user_profile.doctor_consumers.list_doctors_consumers import ListDoctorsConsumers
from video_call.api.consumers import VideoCallConsumers

websocket_urlpatterns = [
    path('ws/accounts/login', LoginConsumers.as_asgi()),

    path('ws/appointments/add_appointment', AddAppointmentConsumer.as_asgi()),
    path('ws/appointments/get_appointments', GetAppointmentConsumer.as_asgi()),
    path('ws/appointments/get_appointment_detail', GetAppointmentDetailConsumer.as_asgi()),
    path('ws/appointments/get_doc_appointment_detail', GetDocAppointmentDetailsConsumer.as_asgi()),
    path('ws/appointments/change_appointment_state', ChangeAppointmentStateConsumer.as_asgi()),

    path('ws/appointments/get_doc_appointment', GetDocAppointmentConsumer.as_asgi()),
    path('ws/appointments/get_doctor_appointment', GetDoctorAppointmentsConsumer.as_asgi()),
    path('ws/appointments/get_appointment_mediums', GetAppointmentMediumConsumers.as_asgi()),
    path('ws/appointments/get_appointment_messages', AppointmentMessageConsumers.as_asgi()),

    path('ws/appointments/add_prescription', AddPrescriptionsConsumer.as_asgi()),
    path('ws/appointments/list_prescriptions', ListPrescriptionsConsumer.as_asgi()),
    path('ws/appointments/list_doc_prescriptions', ListDocPrescriptionsConsumer.as_asgi()),
    path('ws/appointments/list_pat_prescriptions', ListPatPrescriptionsConsumer.as_asgi()),

    path('ws/user_profile/get_patient_profile', GetPatientProfileConsumer.as_asgi()),
    path('ws/user_profile/edit_patient_profile', EditPatientProfileConsumer.as_asgi()),
    path('ws/user_profile/add_time_slot', AddTimeSlotConsumers.as_asgi()),

    path('ws/user_profile/get_doctor_profile', GetDoctorProfileConsumer.as_asgi()),
    path('ws/user_profile/edit_doctor_profile', EditDoctorProfileConsumer.as_asgi()),

    path('ws/user_profile/list_all_doctors', ListDoctorsConsumers.as_asgi()),
    path('ws/user_profile/doctor_details', DoctorDetailConsumers.as_asgi()),

    path('ws/home_page/get_home_data', GetPatientHomeDataConsumer.as_asgi()),
    path('ws/home_page/get_doc_home_data', GetDocHomeDataConsumer.as_asgi()),
    path('ws/home_page/get_admin_home_data', GetAdminHomeDataConsumer.as_asgi()),

    path('ws/posts/get_all_articles', GetAllArticlesConsumers.as_asgi()),
    path('ws/posts/add_article', AddArticleConsumers.as_asgi()),
    path('ws/posts/edit_article', EditArticleConsumers.as_asgi()),

    path('ws/notifications/get_patient_notification', PatientNotificationConsumers.as_asgi()),
    path('ws/notifications/get_doctor_notification', DoctorNotificationConsumers.as_asgi()),


    path('ws/video_call/video_call', VideoCallConsumers.as_asgi()),
    path('ws/search/search_database', SearchConsumers.as_asgi()),

    path('communications/web_video_call/', WebVideoCallConsumers.as_asgi()),
    path('communications/chat_page_admin/', ChatMessagesAdminConsumers.as_asgi()),
    path('communications/chat_page_patient/', ChatMessagesPatConsumers.as_asgi()),
    path('communications/chat_page_doctor/', ChatMessagesDocConsumers.as_asgi()),

    path('appointments/appointment_text_message_page/', AppointmentTextMessagePageConsumers.as_asgi()),

]
