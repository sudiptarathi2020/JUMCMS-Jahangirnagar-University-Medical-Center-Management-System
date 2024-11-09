from django.test import TestCase, Client
from django.urls import reverse
from users.models import Patient, User, Doctor
from medical_tests.models import TestReport, PrescribedTest, Test
from medicines.models import Prescription
from appointments.models import DoctorAppointment
class TestReportViewTests(TestCase):
    """Test suite for views related to viewing and downloading test reports."""
    def setUp(self):
         """Set up the necessary objects for testing TestReport-related views, including users, patient, doctor, and test report."""
        # Create a user and patient
        self.patient_user = User.objects.create_user(
            email='patient@example.com', name='John Doe', role='Student',
            blood_group='B+', date_of_birth='1990-05-10', gender='Male',
            phone_number='+8801987654321', password='asdf1234@'
        )
        self.patient = Patient.objects.create(user=self.patient_user)
        # Create related objects for the test report

        self.doctor_user = User.objects.create_user(
            email='doctor@example.com', name='Doctor', role='Doctor',
            blood_group='A+', date_of_birth='1999-05-10', gender='Male',
            phone_number='+8801711111111', password='asdf1234@'
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor, patient=self.patient,
            appointment_date_time='2024-12-15T10:00:00Z', status='scheduled'
        )
        self.prescription = Prescription.objects.create(
            doctor_appointment= self.appointment,
            complains="Fever",
            vitals="Very Bad",
            diagnosis="Good"
        )
        self.test = Test.objects.create(name="Blood Test", description="Complete blood count")
        self.prescribed_test = PrescribedTest.objects.create(prescription=self.prescription, test = self.test)
        self.test_report = TestReport.objects.create(
            prescribed_test=self.prescribed_test,
            result="Cancer",
            notes="Die"
        )

        self.client = Client()
        self.client.login(username='patient@example.com', password='asdf1234@')

    def test_view_test_report_authenticated(self):
        """Test that authenticated users can access the view_test_report view."""
        response = self.client.get(reverse('medical_tests:view-test-report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/view_test_report.html')
        self.assertIn(self.test_report, response.context['reports'])

    def test_view_test_report_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('medical_tests:view-test-report'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, '/accounts/login/?next=/medical_test/view_test_report/')

    def test_download_test_report_authenticated(self):
        """Test that authenticated users can download a test report."""
        response = self.client.get(reverse('medical_tests:download-test-report', args=[self.test_report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertIn('attachment; filename="TestReport_', response['Content-Disposition'])

    def test_download_test_report_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('medical_tests:download-test-report', args=[self.test_report.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, f'/accounts/login/?next=/medical_test/Download_test_report/{self.test_report.id}/')

    def test_download_test_report_invalid_id(self):
        """Test that accessing an invalid report ID returns a 404."""
        invalid_report_id = 999 
        response = self.client.get(reverse('medical_tests:download-test-report', args=[invalid_report_id]))
        self.assertEqual(response.status_code, 404)