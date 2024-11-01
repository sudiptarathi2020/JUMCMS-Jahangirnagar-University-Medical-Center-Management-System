from django.db import models
from appointments.constants import MEDICAL_TEST_CHOICES
from users.models import Doctor, Patient, LabTechnician


class Appointment(models.Model):
    """
    Abstract model representing a general appointment with attributes common to all types of appointments.

    Attributes:
        patient (ForeignKey): A reference to the Patient model, representing the patient for this appointment.
        appointment_date_time (DateTimeField): Date and time of the appointment.
        status (CharField): Current status of the appointment, limited to either 'scheduled' or 'completed'.
    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[("scheduled", "Scheduled"), ("completed", "Completed")]
    )
    is_emergency = models.BooleanField(
        default=False, help_text="Indicates whether the appointment is emergency."
    )

    class Meta:
        abstract = (
            True  # This model will not be created as a database table, only subclassed.
        )

    def __str__(self):
        """
        String representation of the Appointment object.

        Returns:
            str: A string showing the date and time of the appointment.
        """
        return f"Appointment on {self.appointment_date_time}"


class DoctorAppointment(Appointment):
    """
    Model representing a doctor's appointment, inheriting from the abstract Appointment model.

    Attributes:
        doctor (ForeignKey): A reference to the Doctor model, indicating the doctor assigned to this appointment.
        reason (CharField): A short description or reason for the appointment.
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    reason = models.CharField(max_length=200, default="")

    def __str__(self):
        """
        String representation of the DoctorAppointment object.

        Returns:
            str: A string showing the doctor’s name and the appointment date and time.
        """
        return f"Appointment with Dr. {self.doctor.user.name} on {self.appointment_date_time}"


class TestAppointment(Appointment):
    """
    Model representing a lab test appointment, inheriting from the abstract Appointment model.

    Attributes:
        lab_technician (ForeignKey): A reference to the LabTechnician model, indicating the technician handling the test.
        medical_test (CharField): The type of medical test, with choices defined in MEDICAL_TEST_CHOICES.
    """

    lab_technician = models.ForeignKey(
        LabTechnician, on_delete=models.CASCADE, related_name="test_appointments"
    )
    medical_test = models.CharField(
        max_length=200,
        choices=MEDICAL_TEST_CHOICES,
        default="",
    )

    def __str__(self):
        """
        String representation of the TestAppointment object.

        Returns:
            str: A string showing the lab technician’s username, the appointment date and time, and the medical test type.
        """
        return f"Appointment with {self.lab_technician.user.username} on {self.appointment_date_time} for {self.medical_test}"
