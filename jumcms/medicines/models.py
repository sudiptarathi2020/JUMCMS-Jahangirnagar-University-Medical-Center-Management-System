from django.db import models
from appointments.models import DoctorAppointment
from medicines.constants import *


# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255)
    dosage_form = models.CharField(max_length=100)
    strength = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    expiry_date = models.DateField()
    # prescription_required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.strength})"


class Prescription(models.Model):
    doctor_appointment = models.ForeignKey(
        DoctorAppointment, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    diagnosis = models.TextField()
    date_issued = models.DateField(auto_now_add=True)
    next_visit_date = models.DateField(null=True, blank=True)
    is_referred = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.doctor_appointment.patient.name} by {self.doctor_appointment.doctor.name} on {self.date_issued}"


class PrescribedMedicine(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="medicines"
    )
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE)
    frequency = (
        models.CharField(
            max_length=200,
            choices=MEDICINE_FREQUENCY_CHOICES,
        ),
    )
    duration = models.IntegerField(default=0)
    instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicine.name} for {self.prescription.patient}"
