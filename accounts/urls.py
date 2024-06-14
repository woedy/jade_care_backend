
from django.urls import path, include

from accounts.views import LoginPatientView, RegisterPatientView, logout_patient_view, LoginDoctorView, \
    RegisterDoctorView, logout_doctor_view, RegisterAdminView, LoginAdminView

app_name = "accounts"

urlpatterns = [
    path("login_patient/", LoginPatientView.as_view(), name="login_patient"),
    path("login_doctor/", LoginDoctorView.as_view(), name="login_doctor"),
    path("login_admin/", LoginAdminView.as_view(), name="login_admin"),

    path("logout_patient/", logout_patient_view, name="logout_patient"),
    path("logout_doctor/", logout_doctor_view, name="logout_doctor"),

    path("register_patient/", RegisterPatientView.as_view(), name="register_patient"),
    path("register_doctor/", RegisterDoctorView.as_view(), name="register_doctor"),
    path("register_admin/", RegisterAdminView.as_view(), name="register_admin"),

]
