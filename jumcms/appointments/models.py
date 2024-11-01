from django.db import models
from appointments.constants import *
from users.models import Doctor, Patient, LabTechnician


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[("scheduled", "Scheduled"), ("completed", "Completed")]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Appointment on {self.appointment_date_time}"


class DoctorAppointment(Appointment):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    reason = models.CharField(max_length=200, default=False)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.name} on {self.appointment_date_time}"


class TestAppointment(Appointment):
    lab_technician = models.ForeignKey(
        LabTechnician, on_delete=models.CASCADE, related_name="test_appointments"
    )
    medical_test = models.CharField(
        max_length=200,
        choices=MEDICAL_TEST_CHOICES,
        default=False,
    )

    def __str__(self):
        return f"Appointment with {self.lab_technician.user.name} on {self.appointment_date_time} for {self.medical_test}"
