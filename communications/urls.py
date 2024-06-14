
from django.urls import path, include

from communications.views import text_message_page_pat, video_call_page, chat_page_admin, all_chat_users_admin, \
    all_chat_messages_admin, chat_page_patient, all_chat_users_patient, all_chat_messages_patient, chat_page_doctor

app_name = "communications"

urlpatterns = [
    path("text_messages/", text_message_page_pat, name="text_messages"),
    path("web_video_call/", video_call_page, name="web_video_call"),

    path("chat_page_admin/", chat_page_admin, name="chat_page_admin"),
    path("all_chat_users_admin/", all_chat_users_admin, name="all_chat_users_admin"),
    path("all_chat_messages_admin/", all_chat_messages_admin, name="all_chat_messages_admin"),

    path("chat_page_patient/", chat_page_patient, name="chat_page_patient"),
    path("all_chat_users_patient/", all_chat_users_patient, name="all_chat_users_patient"),
    path("all_chat_messages_patient/", all_chat_messages_patient, name="all_chat_messages_patient"),

    path("chat_page_doctor/", chat_page_doctor, name="chat_page_doctor"),

]