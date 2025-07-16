"""
URL configuration for the `appointments` app.

This module defines URL patterns for managing appointments in the system,
including doctor and test appointments.

Routes:
    - **delete-doctor-appointment/<int:pk>/**: Deletes a specific doctor appointment.
    - **patient-information/<int:pk>/**: Retrieves patient information by patient ID.
    - **create/**: Creates a new doctor appointment.
    - **doctor-appointment-list-for-patient/**: Lists doctor appointments for a specific patient.
    - **test_appointment/reschedule/<int:appointment_id>/**: Reschedules a test appointment.
    - **test_appointments/**: Lists all test appointments.
    - **list/**: Displays the lab technician dashboard.

Attributes:
    urlpatterns (list): A list of URL patterns for the `appointments` app.
"""

from django.urls import path
from appointments.controllers import (
    test_appointments_list,
    reschedule_test_appointment,
    labt_dashboard,
    delete_doctor_appointment,
    get_patient_information,
    create_doctor_appointment,
    get_doctor_appointment_list_for_patient,
)

app_name = "appointments"

urlpatterns = [
    path(
        "delete-doctor-appointment/<int:pk>/",
        delete_doctor_appointment,
        name="delete-doctor-appointment",
    ),
    path(
        "patient-information/<int:pk>/",
        get_patient_information,
        name="patient-information",
    ),
    path("create/", create_doctor_appointment, name="create_doctor_appointment"),
    path(
        "doctor-appointment-list-for-patient/",
        get_doctor_appointment_list_for_patient,
        name="doctor-appointment-list-for-patient",
    ),
    path(
        "test_appointment/reschedule/<int:appointment_id>/",
        reschedule_test_appointment,
        name="reschedule_test_appointment",
    ),
    path("test_appointments/", test_appointments_list, name="test_appointments_list"),
    path("list/", labt_dashboard, name="appointment-list"),
]
