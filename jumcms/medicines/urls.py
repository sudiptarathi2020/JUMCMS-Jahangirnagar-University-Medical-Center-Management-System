from django.urls import path
from medicines.controllers import get_information_for_prescription

app_name = "medicines"
urlpatterns = [
    path(
        "get-information-for-prescription/<int:appointment_id>/",
        get_information_for_prescription,
        name="get-information-for-prescription",
    ),
]
