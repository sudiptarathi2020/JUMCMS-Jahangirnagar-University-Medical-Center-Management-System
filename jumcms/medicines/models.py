from django.db import models
from appointments.models import DoctorAppointment
from medicines.constants import *


# Create your models here.
class Medicine(models.Model):
    """
    Represents a medicine with details such as name, manufacturer, dosage form, and price.

    Fields:
        - name: The brand name of the medicine.
        - generic_name: The generic name of the medicine (optional).
        - manufacturer: The name of the manufacturer.
        - dosage_form: The form in which the medicine is administered (e.g., tablet, syrup).
        - strength: The strength of the medicine (e.g., 500mg).
        - description: Additional details about the medicine (optional).
        - price: The cost of a single unit of the medicine.
        - stock_quantity: The available quantity of the medicine in stock.
        - expiry_date: The expiration date of the medicine.
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

    def __str__(self):
        """
        Returns a string representation of the medicine in the format:
        'Medicine Name (Strength)'.
        """
        return f"{self.name} ({self.strength})"


class Prescription(models.Model):
    """
    Represents a prescription issued during a doctor appointment.

    Fields:
        - doctor_appointment: The associated doctor appointment.
        - complains: The patient's complaints.
        - vitals: The patient's vital signs.
        - diagnosis: The diagnosis made by the doctor.
        - referrals: Any referrals for further consultation or treatment (optional).
        - date_issued: The date the prescription was issued (automatically set).
        - time_issued: The time the prescription was issued (automatically set).
        - next_checkup: The suggested date for the next checkup (optional).
        - is_referred: Indicates if the patient is referred to a specialist.
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
        Returns a string representation of the prescription in the format:
        'Prescription for Patient Name by Doctor Name on Date Issued'.
        """
        return f"Prescription for {self.doctor_appointment.patient.user.name} by {self.doctor_appointment.doctor.user.name} on {self.date_issued}"


class PrescribedMedicine(models.Model):
    """
    Represents a specific medicine prescribed in a prescription.

    Fields:
        - prescription: The associated prescription.
        - medicine: The prescribed medicine.
        - duration: The number of days the medicine should be taken.
        - instructions: Any special instructions for taking the medicine (optional).
        - dosage_frequency: The frequency of dosage (e.g., 'Twice a day').
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
        Returns a string representation of the prescribed medicine in the format:
        'Medicine Name for Patient Name'.
        """
        return f"{self.medicine.name} for {self.prescription.doctor_appointment.patient.user.name}"
