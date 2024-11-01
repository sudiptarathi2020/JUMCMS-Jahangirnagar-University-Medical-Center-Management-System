# appointments/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Patient
from appointments.models import DoctorAppointment
from appointments.forms import DoctorAppointmentCreationForm

User = get_user_model()

class AppointmentsViewsTest(TestCase):
    def setUp(self):
        # Create a test user and patient
        self.user = User.objects.create_user(username='testuser', password='password')
        self.patient = Patient.objects.create(user=self.user)
        self.doctor = Doctor.objects.create(user_id=2)  # Replace with appropriate fields

    def test_create_doctor_appointment_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('create_doctor_appointment'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("create_doctor_appointment")}')

    def test_create_doctor_appointment_success(self):
        self.client.login(username='testuser', password='password')
        
        data = {
            'doctor': self.doctor.id,
            'appointment_date_time': '2024-12-01T10:00',  # Use a valid datetime
            'reason': 'Regular check-up',
            'is_emergency': False,
        }
        response = self.client.post(reverse('create_doctor_appointment'), data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(DoctorAppointment.objects.filter(patient=self.patient).exists())

    def test_get_doctor_appointment_list_for_patient_success(self):
        self.client.login(username='testuser', password='password')
        
        appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time='2024-12-01T10:00',  # Use a valid datetime
            reason='Regular check-up',
            is_emergency=False,
        )

        response = self.client.get(reverse('doctor-appoinement-list-for-patient'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, appointment.reason)

    def test_get_doctor_appointment_list_for_patient_no_appointments(self):
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('doctor-appoinement-list-for-patient'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No appointments found")  # Assuming you have this message in the template
