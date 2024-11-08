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
