"""
URL configuration for the medicines app.

This module defines the URL patterns for the `medicines` app, providing endpoints for handling prescription-related operations.

Routes:
    - `get-information-for-prescription/<int:appointment_id>/`: Fetches information required for creating a prescription.
    - `save-prescription/<int:appointment_id>/`: Saves a prescription for a specific appointment.

Modules:
    - `django.urls.path`: Used to define URL patterns.
    - `medicines.controllers.get_information_for_prescription`: Controller for fetching prescription information.
    - `medicines.controllers.save_prescription`: Controller for saving prescriptions.

"""

from django.urls import path
from medicines.controllers import get_information_for_prescription, save_prescription

app_name = "medicines"
urlpatterns = [
    path(
        "get-information-for-prescription/<int:appointment_id>/",
        get_information_for_prescription,
        name="get-information-for-prescription",
    ),
    path(
        "save-prescription/<int:appointment_id>/",
        save_prescription,
        name="save-prescription",
    ),
]
