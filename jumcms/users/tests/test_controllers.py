from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from appointments.models import DoctorAppointment
from users.models import Doctor, Patient
from django.utils import timezone

User = get_user_model()


class UserControllersTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="Patient",
            blood_group="A+",
            date_of_birth="2000-01-01",
            gender="Male",
            phone_number="+8801234567890",
            password="testpassword123",
        )
        self.user.is_approved = True
        self.user.save()

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/home.htm")

    def test_register_view_valid(self):
        response = self.client.post(
            reverse("users:users-register"),
            {
                "email": "newuser@example.com",
                "name": "New User",
                "role": "Doctor",
                "blood_group": "B+",
                "date_of_birth": "1995-05-05",
                "gender": "Female",
                "phone_number": "+8801987654321",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertTemplateUsed(response, "users/unapproved.htm")
        self.assertIn(
            "Registration successful! Please wait until your account is approved!!",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_register_view_invalid(self):
        response = self.client.post(
            reverse("users:users-register"),
            {
                "email": "",
                "name": "New User",
                "role": "Doctor",
                "blood_group": "B+",
                "date_of_birth": "1995-05-05",
                "gender": "Female",
                "phone_number": "+8801987654321",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_log_in_view_valid(self):
        response = self.client.post(
            reverse("users:users-login"),
            {"username": "testuser@example.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_log_in_view_invalid(self):
        response = self.client.post(
            reverse("users:users-login"),
            {"username": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.htm")
        self.assertIn(
            "Invalid email or password",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_log_out_view(self):
        self.client.login(username="testuser@example.com", password="testpassword123")
        response = self.client.get(reverse("users:users-logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# Doctor part start
class DoctorDashboardControllerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="doctoruser@example.com",
            name="Doctor User",
            role="doctor",
            blood_group="B+",
            date_of_birth="1985-05-05",
            gender="Female",
            phone_number="+8800987654321",
            password="password123",
        )
        self.user2 = User.objects.create_user(
            email="patientuser@example.com",
            name="Patient User",
            role="patient",
            blood_group="B+",
            date_of_birth="1985-05-05",
            gender="Female",
            phone_number="+8800987654321",
            password="password123",
        )
        self.doctor = Doctor.objects.create(user=self.user)
        self.patient = Patient.objects.create(user=self.user2)
        self.appointment_today = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=timezone.now(),
        )
        self.appointment_future = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=timezone.now() + timezone.timedelta(days=1),
        )
        self.appointment_past = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=timezone.now() - timezone.timedelta(days=1),
        )

    def test_doctor_dashboard_access_logged_in(self):
        self.client.login(email="doctoruser@example.com", password="password123")

        response = self.client.get(reverse("users:doctor-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctors/doctor_dashboard.htm")

        self.assertIn("doctor", response.context)
        self.assertEqual(response.context["doctor"], self.doctor)
        self.assertIn("appointments_today", response.context)
        self.assertEqual(len(response.context["appointments_today"]), 1)

    def test_doctor_dashboard_access_for_non_doctor_user(self):
        User.objects.create_user(
            email="nondoctoruser@example.com",
            name="Non doctor",
            role="doctor",
            blood_group="B+",
            date_of_birth="1985-05-05",
            gender="Female",
            phone_number="+8800987654321",
            password="password123",
        )
        self.client.login(email="nondoctoruser@example.com", password="password123")

        response = self.client.get(reverse("users:doctor-dashboard"))
        self.assertEqual(response.status_code, 404)

    def test_doctor_dashboard_context_data(self):
        self.client.login(email="doctoruser@example.com", password="password123")

        response = self.client.get(reverse("users:doctor-dashboard"))
        self.assertEqual(response.status_code, 200)

        appointments_data = response.context["appointments_data"]
        expected_appointments_data = [0] * 10 + [3, 0]
        self.assertEqual(appointments_data, expected_appointments_data)


# Doctor part end
