"""
URL Configuration for the Appointments Module.

This module defines the URL patterns for managing doctor appointments and patient information.

.. module:: appointments.urls
   :synopsis: URL configuration for the Appointments app.

Attributes
----------
urlpatterns : list
    A list of URL patterns that maps URLs to their corresponding view functions.

Routes
------
- **delete-doctor-appointment/<int:pk>/**  
  Deletes a specific doctor appointment based on its primary key.

  - **View**: `delete_doctor_appointment`
  - **Name**: `delete-doctor-appointment`

- **patient-information/<int:pk>/**  
  Retrieves detailed information for a specific patient based on their primary key.

  - **View**: `get_patient_information`
  - **Name**: `patient-information`

- **create/**  
  Creates a new doctor appointment.

  - **View**: `create_doctor_appointment`
  - **Name**: `create_doctor_appointment`

- **doctor-appointment-list-for-patient/**  
  Retrieves the list of doctor appointments for a specific patient.

  - **View**: `get_doctor_appointment_list_for_patient`
  - **Name**: `doctor-appointment-list-for-patient`
"""

from django.urls import path
from appointments.controllers import delete_doctor_appointment, get_patient_information
from .controllers import (
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
]
