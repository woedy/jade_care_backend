
from django.urls import path, include

from prescriptions.views import prescriptions_view

app_name = "prescriptions"

urlpatterns = [
    path("", prescriptions_view, name="prescriptions"),

]
