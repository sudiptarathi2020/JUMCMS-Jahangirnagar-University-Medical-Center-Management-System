from django.urls import path
from appointments.controllers import delete_doctor_appointment

urlpatterns = [
    path(
        "delete-doctor-appointment/<int:pk>/",
        delete_doctor_appointment,
        name="delete-doctor-appointment",
    ),
]
