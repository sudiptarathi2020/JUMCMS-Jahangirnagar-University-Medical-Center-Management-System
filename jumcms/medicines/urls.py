"""
URL configuration for the `medicines` app.

This module defines the URL patterns for managing prescriptions and medicines.
Each endpoint is associated with a specific view function to handle the corresponding action.

Routes:
    - `prescriptions/`:
        Retrieve all prescriptions.
        View: `all_prescriptions`

    - `search/`:
        Search for prescriptions.
        View: `search_prescriptions`

    - `prescription-details/<int:prescription_id>/`:
        Retrieve details of a specific prescription by its ID.
        View: `prescription_details`
        Parameters:
            - prescription_id (int): The ID of the prescription.

    - `dispense/<int:prescription_id>/`:
        Dispense medicines for a specific prescription by its ID.
        View: `dispense_medicines`
        Parameters:
            - prescription_id (int): The ID of the prescription.

    - `add-medicine/`:
        Add a new medicine to the system.
        View: `add_medicine`

    - `get-information-for-prescription/<int:appointment_id>/`:
        Get prescription-related information for a specific appointment.
        View: `get_information_for_prescription`
        Parameters:
            - appointment_id (int): The ID of the appointment.

    - `save-prescription/<int:appointment_id>/`:
        Save a prescription for a specific appointment.
        View: `save_prescription`
        Parameters:
            - appointment_id (int): The ID of the appointment.

Attributes:
    app_name (str): The namespace for the `medicines` app.
    urlpatterns (list): List of URL patterns for the app.
"""

from django.urls import path
from medicines.controllers import (
    get_information_for_prescription,
    save_prescription,
    prescription_details,
    search_prescriptions,
    all_prescriptions,
    dispense_medicines,
    add_medicine,
)

app_name = "medicines"
urlpatterns = [
    path("prescriptions", all_prescriptions, name="all_prescriptions"),
    path("search/", search_prescriptions, name="search-prescriptions"),
    path(
        "prescription-details/<int:prescription_id>/",
        prescription_details,
        name="prescription-details",
    ),
    path(
        "dispense/<int:prescription_id>/", dispense_medicines, name="dispense-medicines"
    ),
    path("add-medicine/", add_medicine, name="add-medicine"),
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
