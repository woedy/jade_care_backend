
from django.urls import path, include

from home_page.views import home_page, patient_home_page, doctor_home_page, admin_home_page

app_name = "home_page"

urlpatterns = [
    path("", home_page, name="home_page"),
    path("patient_home/", patient_home_page, name="patient_home"),
    path("doctor_home/", doctor_home_page, name="doctor_home"),
    path("admin_home/", admin_home_page, name="admin_home"),

]
