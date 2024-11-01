from django.db import models
from appointments.constants import *
from users.models import Doctor, Patient, LabTechnician


class Appointment(models.Model):
    """
    An abstract base model for appointments.

    This model serves as a base class for specific appointment types (e.g., 
    doctor appointments, test appointments). It includes common fields for all 
    appointment types, such as the patient associated with the appointment, 
    the date and time of the appointment, and its status.

    Attributes:
        patient (ForeignKey): The patient associated with the appointment.
        appointment_date_time (DateTimeField): The date and time of the appointment.
        status (CharField): The status of the appointment, either "scheduled" or "completed".

    Meta:
        abstract (bool): Indicates that this model is abstract and should not 
                         be created as a separate table in the database.
    """
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
    """
    Model representing a doctor appointment.

    This model extends the Appointment abstract base model to include 
    specific fields for doctor appointments, such as the associated doctor 
    and the reason for the appointment.

    Attributes:
        doctor (ForeignKey): The doctor associated with the appointment.
        reason (CharField): The reason for the appointment.

    Methods:
        __str__(): Returns a string representation of the doctor appointment.
    """
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    reason = models.CharField(max_length=200, default=False)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.name} on {self.appointment_date_time}"


class TestAppointment(Appointment):
    """
    Model representing a medical test appointment.

    This model extends the Appointment abstract base model to include 
    specific fields for test appointments, such as the associated lab technician 
    and the type of medical test being performed.

    Attributes:
        lab_technician (ForeignKey): The lab technician associated with the appointment.
        medical_test (CharField): The type of medical test associated with the appointment.

    Methods:
        __str__(): Returns a string representation of the test appointment.
    """
    lab_technician = models.ForeignKey(
        LabTechnician, on_delete=models.CASCADE, related_name="test_appointments"
    )
    medical_test = models.CharField(
        max_length=200,
        choices=MEDICAL_TEST_CHOICES,
        default=False,
    )

    def __str__(self):
        return f"Appointment with {self.lab_technician.user.username} on {self.appointment_date_time} for {self.medical_test}"
