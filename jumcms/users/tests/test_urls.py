from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from users.controllers import register, log_in, log_out
from users.models import User, Doctor


class UserTestUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse("users-register")
        resolved = resolve(url)
        self.assertEqual(resolved.func, register)

    def test_login_url_is_resolved(self):
        url = reverse("users-login")
        resolved = resolve(url)
        self.assertEqual(resolved.func, log_in)

    def test_logout_url_is_resolved(self):
        url = reverse("users-logout")
        resolved = resolve(url)
        self.assertEqual(resolved.func, log_out)


# Doctor part start
class DoctorDashboardURLsTest(TestCase):
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
        self.doctor = Doctor.objects.create(user=self.user, no_of_appointments=5)

    def test_doctor_dashboard_url(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        url = reverse("doctor-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_doctor_dashboard_access_invalid_user(self):
        non_doctor_user = User.objects.create_user(
            email="non_doctor@example.com",
            name="Non-Doctor User",
            role="patient",
            blood_group="B+",
            date_of_birth="1985-05-05",
            gender="Female",
            phone_number="+8800987654321",
            password="password123",
        )
        self.client.login(email="non_doctor@example.com", password="password123")
        url = reverse("doctor-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# Doctor part end
