
from django.urls import path, include

from medical_centers.views import medical_centers_view
from prescriptions.views import prescriptions_view

app_name = "medical_centers"

urlpatterns = [
    path("", medical_centers_view, name="medical_centers"),

]
