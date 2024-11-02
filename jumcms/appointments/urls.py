"""
URL configuration for the appointments app.

This module defines the URL patterns for the appointments app,
specifying the routes and their corresponding views.

The following URL patterns are defined:

- `delete-doctor-appointment/<int:pk>/`: Deletes a doctor's appointment using the primary key (pk).
- `patient-information/<int:pk>/`: Retrieves patient information using the primary key (pk).

Usage:
    Include this URL configuration in your project's main `urls.py` file:
    
    ```python
    from django.urls import include, path
    
    urlpatterns = [
        path('appointments/', include('appointments.urls')),
    ]
    ```

"""

from django.urls import path
from appointments.controllers import delete_doctor_appointment, get_patient_information

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
]
