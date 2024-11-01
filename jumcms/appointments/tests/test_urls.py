from django.test import TestCase
from django.urls import reverse
from appointments.models import DoctorAppointment
from users.models import User, Patient, Doctor


class AppointmentsURLsTest(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="patient",
            blood_group="O+",
            date_of_birth="1990-01-01",
            gender="Male",
            phone_number="+8801234567890",
            password="password123",
        )
        self.doctor = Doctor.objects.create(user=self.user, no_of_appointments=0)
        self.patient = Patient.objects.create(user=self.user)
        self.appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time="2024-11-02 10:00:00",
            status="scheduled",
            reason="Routine checkup",
        )

    def test_delete_doctor_appointment_url(self):
        url = reverse("delete-doctor-appointment", args=[self.appointment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)  # Check if redirect after deletion

    def test_patient_information_url(self):
        url = reverse("patient-information", args=[self.appointment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.user.name)

    def test_invalid_delete_url(self):
        url = reverse("delete-doctor-appointment", args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_patient_information_url(self):
        url = reverse("patient-information", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
