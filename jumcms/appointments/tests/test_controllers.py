from django.test import TestCase, Client
from django.urls import reverse

from appointments.forms import DoctorAppointmentCreationForm
from appointments.models import DoctorAppointment  # Assuming your appointments app is named 'appointments'
from users.models import Patient, Doctor, User


class CreateDoctorAppointmentTestCase(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.test_appointment = None

    def setUp(self):
        self.client = Client()

        # Create a Lab Technician user and instance
        self.lab_technician_user = User.objects.create_user(
            email='labt@example.com', name='Lab Technician', role='Lab_technician',
            blood_group='A+', date_of_birth='1980-01-01', gender='Male',
            phone_number='+8801712345678', password='asdf1234@'
        )

        # Create a Patient user and instance
        self.patient_user = User.objects.create_user(
            email='patient@example.com', name='John Doe', role='Student',
            blood_group='B+', date_of_birth='1990-05-10', gender='Male',
            phone_number='+8801987654321', password='asdf1234@'
        )
        self.patient_user.is_approved = True
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create a Doctor user and instance
        self.doctor_user = User.objects.create_user(
            email='doctor@example.com', name='Dr. Example', role='Doctor',
            blood_group='O+', date_of_birth='1975-08-15', gender='Male',
            phone_number='+8801812345678', password='asdf1234@'
        )
        self.doctor_user.is_approved = True
        self.doctor = Doctor.objects.create(user=self.doctor_user, no_of_appointments=0)

        # Create a test appointment
        # Define URLs for test cases
        self.url = reverse('appointments:create_doctor_appointment')

    def test_patient_required(self):
        # Create a user who is not a patient
        self.client.force_login(self.lab_technician_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('users:users-login'))  # Check redirect URL
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You must be a registered patient to make an appointment.")

    def test_get_request(self):
        self.client.login(username='patient@example.com', password='asdf1234@')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/make_doctor_appointment.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], DoctorAppointmentCreationForm)

    def test_post_request_invalid_form(self):
        self.client.login(username='patient@example.com', password='asdf1234@')
        # Create invalid form data (e.g., missing required field)
        invalid_form_data = {
            'appointment_date_time': '2024-12-25 10:00:00',
            'reason': 'Regular checkup',
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/make_doctor_appointment.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)  # Check for form errors

    def test_get_appointments_for_patient(self):
        self.client.login(username='patient@example.com', password='asdf1234@')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
        'patients/make_doctor_appointment.html')