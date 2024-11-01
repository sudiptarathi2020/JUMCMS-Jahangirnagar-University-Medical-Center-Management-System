from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime
from users.models import LabTechnician, Patient, Doctor, User
from appointments.models import TestAppointment


class TestAppointmentsViews(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a Lab Technician user and instance
        self.lab_technician_user = User.objects.create_user(
            email='labt@example.com', name='Lab Technician', role='Lab_technician',
            blood_group='A+', date_of_birth='1980-01-01', gender='Male',
            phone_number='+8801712345678', password='asdf1234@'
        )
        self.lab_technician = LabTechnician.objects.create(user=self.lab_technician_user)

        # Create a Patient user and instance
        self.patient_user = User.objects.create_user(
            email='patient@example.com', name='John Doe', role='Student',
            blood_group='B+', date_of_birth='1990-05-10', gender='Male',
            phone_number='+8801987654321', password='asdf1234@'
        )
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create a Doctor user and instance
        self.doctor_user = User.objects.create_user(
            email='doctor@example.com', name='Dr. Example', role='Doctor',
            blood_group='O+', date_of_birth='1975-08-15', gender='Male',
            phone_number='+8801812345678', password='asdf1234@'
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user, no_of_appointments=0)

        # Create a test appointment
        self.appointment = TestAppointment.objects.create(
            lab_technician=self.lab_technician,
            patient=self.patient,
            appointment_date_time='2024-12-15T10:00:00Z',
            status='scheduled',
            medical_test='blood_test'
        )

        # Define URLs for test cases
        self.login_url = reverse('users:users-login')
        self.dashboard_url = reverse('appointments:test_appointments_list')
        self.reschedule_url = reverse('appointments:reschedule_test_appointment', args=[self.appointment.id])

    def test_lab_technician_access_dashboard(self):
        # Log in as the lab technician and access the dashboard
        self.client.login(email='labt@example.com', password='asdf1234@')
        response = self.client.get(self.dashboard_url)

        # Verify successful dashboard access and correct template usage
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['lab_technician/lab_technician_dashboard_list.htm'])
        self.assertEqual('appointments' in response.context, True)
        self.assertEqual(self.appointment in response.context['appointments'], True)

    def test_dashboard_access_denied_for_non_lab_technician(self):
        # Log in as a non-lab technician user and attempt to access the dashboard
        self.client.login(email='patient@example.com', password='asdf1234@')
        response = self.client.get(self.dashboard_url)

        # Verify redirection to login page with an error message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(any("You do not have permission" in str(message) for message in messages), True)

    def test_dashboard_template_for_get_request(self):
        # Log in as the lab technician and send a GET request to the dashboard
        self.client.login(email='labt@example.com', password='asdf1234@')
        response = self.client.get(self.dashboard_url)

        # Verify correct template is used and no appointments context for GET requests
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['lab_technician/lab_technician_dashboard.htm'])
        self.assertEqual('appointments' in response.context, False)

    def test_reschedule_appointment_page_access(self):
        # Log in as the lab technician and access the reschedule page for an appointment
        self.client.login(email='labt@example.com', password='asdf1234@')
        response = self.client.get(self.reschedule_url)

        # Verify successful access to the rescheduling page and correct template usage
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['appointments/reschedule_test_appointment.htm'])
        self.assertEqual(response.context['appointment'], self.appointment)
