from django.test import TestCase, Client
from django.urls import reverse

from appointments.models import TestAppointment
from medical_tests.models import Test
from users.models import LabTechnician, Patient, Doctor, User


class TestAppointmentsViews(TestCase):
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
        self.lab_technician_user.is_approved = True
        self.lab_technician = LabTechnician.objects.create(user=self.lab_technician_user)

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

        self.temporary_test = Test.objects.create(
            name="blood_test"
        )
        # Create a test appointment
        self.appointment = TestAppointment.objects.create(
            lab_technician=self.lab_technician,
            patient=self.patient,
            appointment_date_time='2024-12-15T10:00:00Z',
            status='scheduled',
            medical_test=self.temporary_test
        )

        # Define URLs for test cases
        self.login_url = reverse('users:users-login')
        self.dashboard_url = reverse('appointments:test_appointments_list')
        self.reschedule_url = reverse('appointments:reschedule_test_appointment', args=[self.appointment.id])
    def test_login_required(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_get_request(self):
        self.client.login(username='labt@example.com', password='asdf1234@')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code,
        200)
        self.assertTemplateUsed(response,
        'lab_technician/lab_technician_dashboard.htm')

    def test_post_request_valid_user(self):
        self.client.login(username='labt@example.com', password='asdf1234@')
        response = self.client.post(self.dashboard_url)
        self.assertEqual(response.status_code,
        200)
        self.assertTemplateUsed(response, 'lab_technician/lab_technician_dashboard_list.htm')
        self.assertIn('appointments', response.context)
        self.assertIn('lab_technician', response.context)

    def test_post_request_invalid_user(self):
        self.client.login(username='labt@example.com', password='asdf1234@')
        # Create a new user who is not a lab technician
        self.client.force_login(self.patient_user)  # Force login as the new user
        response = self.client.post(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('users:users-login'))

    def test_post_request_valid_user_valid_form(self):
        self.client.login(username='labt@example.com', password='asdf1234@')
        new_date_time = '2024-12-15T10:00:00Z'  # Example new date
        response = self.client.post(self.reschedule_url, {'appointment_date': self.appointment.appointment_date_time})  # Adjust form data as needed
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_technician/reschedule_test_appointment.html')
        self.assertEqual(str(self.appointment.appointment_date_time), new_date_time)