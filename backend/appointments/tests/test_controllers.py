from django.test import TestCase, Client
from django.urls import reverse
from medical_tests.models import Test
from users.models import LabTechnician, Patient, Doctor, User
from appointments.models import DoctorAppointment, TestAppointment
from users.models import User, Patient, Doctor
from datetime import date
from django.utils import timezone
from appointments.controllers import get_doctor_appointments, calculate_detailed_age
from appointments.forms import DoctorAppointmentCreationForm


# Doctor part start
class DoctorAppointmentControllersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="patient",
            blood_group="O+",
            date_of_birth="1998-11-02",
            gender="Male",
            phone_number="+8801234567890",
            role_id = "aaaaaa",
            password="password123",
        )
        self.doctor = Doctor.objects.create(user=self.user, no_of_appointments=0)
        self.patient = Patient.objects.create(user=self.user)
        self.appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=timezone.now() + timezone.timedelta(days=1),
            status="scheduled",
            reason="Routine checkup",
        )

    def test_get_doctor_appointments(self):
        appointments = get_doctor_appointments(self.doctor)
        self.assertIn(self.appointment, appointments)

        # Test with no appointments
        DoctorAppointment.objects.all().delete()
        appointments = get_doctor_appointments(self.doctor)
        self.assertEqual(appointments.count(), 0)

    def test_delete_doctor_appointment(self):
        response = self.client.delete(
            reverse(
                "appointments:delete-doctor-appointment", args=[self.appointment.pk]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            DoctorAppointment.objects.filter(pk=self.appointment.pk).exists()
        )

    def test_get_patient_information(self):
        response = self.client.get(
            reverse("appointments:patient-information", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctors/patient_information.htm")
        self.assertContains(response, self.patient.user.name)

    def test_calculate_detailed_age(self):
        dob = date(1998, 11, 2)
        date_today = date(2024, 11, 11)
        expected_age = "26 years, 0 months, 9 days"
        self.assertEqual(calculate_detailed_age(dob, date_today), expected_age)

    def test_age_on_birthday_today(self):
        dob = timezone.now().date()
        self.assertEqual(
            calculate_detailed_age(dob, timezone.now().date()),
            "0 years, 0 months, 0 days",
        )


# Doctor part end


class CreateDoctorAppointmentTestCase(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.test_appointment = None

    def setUp(self):
        self.client = Client()

        # Create a Lab Technician user and instance
        self.lab_technician_user = User.objects.create_user(
            email="labt@example.com",
            name="Lab Technician",
            role="Lab_technician",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            role_id = "bbbbbb",
            password="asdf1234@",
        )

        # Create a Patient user and instance
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            role_id = "cccccc",
            password="asdf1234@",
        )
        self.patient_user.is_approved = True
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create a Doctor user and instance
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Example",
            role="Doctor",
            blood_group="O+",
            date_of_birth="1975-08-15",
            gender="Male",
            phone_number="+8801812345678",
            role_id = "gggggg",
            password="asdf1234@",
        )
        self.doctor_user.is_approved = True
        self.doctor = Doctor.objects.create(user=self.doctor_user, no_of_appointments=0)

        # Create a test appointment
        # Define URLs for test cases
        self.url = reverse("appointments:create_doctor_appointment")

    def test_patient_required(self):
        # Create a user who is not a patient
        self.client.force_login(self.lab_technician_user)
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("users:users-login")
        )  # Check redirect URL
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You must be a registered patient to make an appointment."
        )

    def test_get_request(self):
        self.client.login(username="patient@example.com", password="asdf1234@")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patients/make_doctor_appointment.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], DoctorAppointmentCreationForm)

    def test_post_request_invalid_form(self):
        self.client.login(username="patient@example.com", password="asdf1234@")
        # Create invalid form data (e.g., missing required field)
        invalid_form_data = {
            "appointment_date_time": "2024-12-25 10:00:00",
            "reason": "Regular checkup",
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patients/make_doctor_appointment.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)  # Check for form errors

    def test_get_appointments_for_patient(self):
        self.client.login(username="patient@example.com", password="asdf1234@")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patients/make_doctor_appointment.html")


class TestAppointmentsViews(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.test_appointment = None

    def setUp(self):
        self.client = Client()

        # Create a Lab Technician user and instance
        self.lab_technician_user = User.objects.create_user(
            email="labt@example.com",
            name="Lab Technician",
            role="Lab_technician",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            role_id = "hhhhhh",
            password="asdf1234@",
        )
        self.lab_technician_user.is_approved = True
        self.lab_technician = LabTechnician.objects.create(
            user=self.lab_technician_user
        )

        # Create a Patient user and instance
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            role_id = "kkkkk",
            password="asdf1234@",
        )
        self.patient_user.is_approved = True
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create a Doctor user and instance
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Example",
            role="Doctor",
            blood_group="O+",
            date_of_birth="1975-08-15",
            gender="Male",
            phone_number="+8801812345678",
            role_id = "mmmmmm",
            password="asdf1234@",
        )
        self.doctor_user.is_approved = True
        self.doctor = Doctor.objects.create(user=self.doctor_user, no_of_appointments=0)

        self.temporary_test = Test.objects.create(name="blood_test")
        # Create a test appointment
        self.appointment = TestAppointment.objects.create(
            lab_technician=self.lab_technician,
            patient=self.patient,
            appointment_date_time="2024-12-15T10:00:00Z",
            status="scheduled",
            medical_test=self.temporary_test,
        )

        # Define URLs for test cases
        self.login_url = reverse("users:users-login")
        self.dashboard_url = reverse("appointments:test_appointments_list")
        self.reschedule_url = reverse(
            "appointments:reschedule_test_appointment", args=[self.appointment.id]
        )

    def test_login_required(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_get_request(self):
        self.client.login(username="labt@example.com", password="asdf1234@")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lab_technician/lab_technician_dashboard.htm")

    def test_post_request_valid_user(self):
        self.client.login(username="labt@example.com", password="asdf1234@")
        response = self.client.post(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "lab_technician/lab_technician_dashboard_list.htm"
        )
        self.assertIn("appointments", response.context)
        self.assertIn("lab_technician", response.context)

    def test_post_request_invalid_user(self):
        self.client.login(username="labt@example.com", password="asdf1234@")
        # Create a new user who is not a lab technician
        self.client.force_login(self.patient_user)  # Force login as the new user
        response = self.client.post(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse("users:users-login"))

    def test_post_request_valid_user_valid_form(self):
        self.client.login(username="labt@example.com", password="asdf1234@")
        new_date_time = "2024-12-15T10:00:00Z"  # Example new date
        response = self.client.post(
            self.reschedule_url,
            {"appointment_date": self.appointment.appointment_date_time},
        )  # Adjust form data as needed
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "lab_technician/reschedule_test_appointment.html"
        )
        self.assertEqual(str(self.appointment.appointment_date_time), new_date_time)
