# appointments/urls.py

from django.urls import path
from .controllers import create_doctor_appointment, appointment_list



urlpatterns = [
    path("create/", create_doctor_appointment, name="create_doctor_appointment"),
    path("list/", appointment_list, name="appointment_list"),
]
