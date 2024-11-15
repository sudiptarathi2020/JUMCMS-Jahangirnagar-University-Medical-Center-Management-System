from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from appointments.models import DoctorAppointment
from users.models import User, Doctor, Patient


# Doctor part start
class DoctorAppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="patient",
            blood_group="O+",
            date_of_birth="1990-01-01",
            gender="Male",
            phone_number="+8801234567890",
            role_id = "aaaaaa",
            password="password123",
        )
        self.doctor_user = User.objects.create_user(
            email="doctoruser@example.com",
            name="Doctor User",
            role="doctor",
            blood_group="B+",
            date_of_birth="1985-05-05",
            gender="Female",
            phone_number="+8800987654321",
            role_id = "bbbbb",
            password="password123",
        )
        self.patient_user = User.objects.create_user(
            email="patientuser@example.com",
            name="Patient User",
            role="patient",
            blood_group="A+",
            date_of_birth="1992-02-02",
            gender="Male",
            phone_number="+8800147852364",
            role_id = "ccccc",
            password="password123",
        )

        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            qualifications="MBBS",
            specialty="Cardiology",
            experience_years=5,
        )

        self.patient = Patient.objects.create(user=self.patient_user)

    def test_doctor_appointment_creation(self):
        """Test creating a DoctorAppointment."""
        appointment_date = timezone.now() + timezone.timedelta(days=1)
        appointment = DoctorAppointment(
            patient=self.patient,
            appointment_date_time=appointment_date,
            status="scheduled",
            doctor=self.doctor,
            reason="Routine checkup",
        )
        appointment.full_clean()
        appointment.save()
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.reason, "Routine checkup")
        self.assertEqual(appointment.status, "scheduled")

    def test_doctor_appointment_str(self):
        """Test the string representation of DoctorAppointment."""
        appointment_date = timezone.now() + timezone.timedelta(days=1)
        appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            appointment_date_time=appointment_date,
            status="scheduled",
            doctor=self.doctor,
            reason="Routine checkup",
        )
        self.assertEqual(
            str(appointment),
            f"Appointment with Dr. {self.doctor.user.name} on {appointment_date}",
        )

    def test_invalid_appointment_status(self):
        """Test creating a DoctorAppointment with an invalid status."""
        appointment_date = timezone.now() + timezone.timedelta(days=1)
        appointment = DoctorAppointment(
            patient=self.patient,
            appointment_date_time=appointment_date,
            status="invalid_status",
            doctor=self.doctor,
            reason="Routine checkup",
        )
        with self.assertRaises(ValidationError):
            appointment.full_clean()

    def test_appointment_date_in_past(self):
        """Test creating a DoctorAppointment with a past date."""
        appointment_date = timezone.now() - timezone.timedelta(days=1)
        appointment = DoctorAppointment(
            patient=self.patient,
            appointment_date_time=appointment_date,
            status="scheduled",
            doctor=self.doctor,
            reason="Routine checkup",
        )
        with self.assertRaises(ValidationError):
            appointment.full_clean()


# Doctor part end
