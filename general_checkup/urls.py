
from django.urls import path, include

from general_checkup.views import general_checkup_view

app_name = "general_checkup"

urlpatterns = [
    path("", general_checkup_view, name="general_checkup"),

]
