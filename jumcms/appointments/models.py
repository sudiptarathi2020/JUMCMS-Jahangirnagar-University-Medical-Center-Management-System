from django.db import models
from users.models import Doctor, Patient, LabTechnician


# Create your models here.
class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    appointment_date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[("scheduled", "Scheduled"), ("completed", "Completed")]
    )

    def __str__(self):
        return (
            f"Appointment with Dr. {self.doctor.user.name} on {self.appointment_date}"
        )


class TestAppointment(models.Model):
    lab_technician = models.ForeignKey(
        LabTechnician, on_delete=models.CASCADE, related_name="test_appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="test_appointments"
    )
    appointment_date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[("scheduled", "Scheduled"), ("completed", "Completed")]
    )

    def __str__(self):
        return f"Appointment with {self.lab_technician.user.username} on {self.appointment_date}"
