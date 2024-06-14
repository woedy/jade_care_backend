from django.urls import path

from accounts.api.views.admin_views import registration_admin_view, ObtainAdminAuthTokenView
from accounts.api.views.doc_views import doc_registration_view, ObtainDocAuthTokenView, logout_doc_view_api
from accounts.api.views.patient_views import patient_registration_view, ObtainPatientAuthTokenView, \
    logout_patient_view_api, patient_registration_validate_email

app_name = 'accounts'

urlpatterns = [
    path('register_patient', patient_registration_view, name="register_patient"),
    path('patient_registration_validate_email', patient_registration_validate_email,
         name="patient_registration_validate_email"),

    path('register_doc', doc_registration_view, name="register_doc"),
    path('register_admin', registration_admin_view, name="register_admin"),

    path('login_patient', ObtainPatientAuthTokenView.as_view(), name="login_patient"),
    path('login_doc', ObtainDocAuthTokenView.as_view(), name="login_doc"),
    path('login_admin', ObtainAdminAuthTokenView.as_view(), name="login_admin"),

    path('logout_patient', logout_patient_view_api, name="logout_patient"),
    path('logout_doc', logout_doc_view_api, name="logout_doc"),
    path('logout_admin', logout_doc_view_api, name="logout_admin"),
    #path('email/resend-activation/', account_email_activation_view, name="resend-activation'"),
    #path('password/change_password/', change_password_view, name="change_password"),
]
