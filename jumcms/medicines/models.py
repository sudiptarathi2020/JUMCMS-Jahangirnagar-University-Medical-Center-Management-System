from django.db import models
from appointments.models import DoctorAppointment
from medicines.constants import *


# Create your models here.
class Medicine(models.Model):
    """
    Medicine Model
    """

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
        """
        string representation of medicine
        :return: String
        """
        return f"{self.name} ({self.strength})"


class Prescription(models.Model):
    """
    Prescription Model
    """

    doctor_appointment = models.ForeignKey(
        DoctorAppointment, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    complains = models.TextField(null=False, max_length=600)
    vitals = models.TextField(null=False, max_length=600)
    diagnosis = models.TextField(null=False, max_length=600)
    referrals = models.TextField(default="")
    date_issued = models.DateField(auto_now_add=True)
    time_issued = models.TimeField(auto_now_add=True)
    next_checkup = models.DateField(null=True, blank=True)
    is_referred = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of prescription
        :return: String
        """
        return f"Prescription for {self.doctor_appointment.patient.user.name} by {self.doctor_appointment.doctor.user.name} on {self.date_issued}"


class PrescribedMedicine(models.Model):
    """
    Prescribed Medicine Model
    """

    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="medicines"
    )
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    instructions = models.TextField(null=True, blank=True)
    dosage_frequency = models.CharField(
        max_length=200, choices=MEDICINE_FREQUENCY_CHOICES, default=""
    )

    def __str__(self):
        """
        String representation of prescribed medicine
        :return: String
        """
        return f"{self.medicine.name} for {self.prescription.doctor_appointment.patient.user.name}"
