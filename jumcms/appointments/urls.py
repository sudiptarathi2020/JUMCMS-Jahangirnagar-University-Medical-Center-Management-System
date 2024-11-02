from django.urls import path
from .controllers import (
    create_doctor_appointment,
    get_doctor_appointment_list_for_patient,
)
app_name = 'appointments'

urlpatterns = [
    path("create/", create_doctor_appointment, name="create_doctor_appointment"),
    path(
        "doctor-appoinement-list-for-patient/",
        get_doctor_appointment_list_for_patient,
        name="doctor-appointment-list-for-patient",
    ),
]
