from django.test import TestCase, Client
from users.models import LabTechnician
from medical_tests.models import PrescribedTest, TestReport, Test
from medicines.models import Prescription
from users.models import Patient, User, Doctor, LabTechnician
from appointments.models import DoctorAppointment
from django.urls import reverse
from django.utils import timezone 
from django.core.files.uploadedfile import SimpleUploadedFile

class LabTechnicianViewsTest(TestCase):
    def setUp(self):
        # Create a test user (Lab Technician)
        self.doctor_user = User.objects.create_user(
            email='doctor@example.com', name='Dr. Sudipta', role='Doctor',
            blood_group='A+', date_of_birth='1980-01-01', gender='Male',
            phone_number='+8801712345678', password='asdf1234@'
        )
        self.patient_user = User.objects.create_user(
            email='patient@example.com', name='John Doe', role='Student',
            blood_group='B+', date_of_birth='1990-05-10', gender='Male',
            phone_number='+8801987654321', password='asdf1234@'
        )

        

        self.lab_technician_user = User.objects.create_user(
            email='labt@example.com', name = 'lab technician', role = 'Lab_technician',
            blood_group = 'A+', date_of_birth= '2000-04-04', gender= 'Male',
            phone_number = '+8801711111111', password = 'asdf1234@'
        )
        self.lab_technician = LabTechnician.objects.create(user = self. lab_technician_user)
        # Create doctor and patient instances
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(user=self.patient_user)

        self.doctor_appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor = self.doctor,
            appointment_date_time='2000-05-05T10:10:10Z',
        )
        
        # Create a test patient, doctor, and prescription
        self.prescription = Prescription.objects.create(
            doctor_appointment=self.doctor_appointment,
            date_issued=timezone.now(), 
            diagnosis="HEPA"
        )
        self.test = Test.objects.create(
            name='CBC',
            description="cancer'"
        )
        # Create a test prescribed test
        self.prescribed_test = PrescribedTest.objects.create(
            prescription=self.prescription,
            test = self.test,
        )

        # Create a test client
        self.client = Client()
        self.client.login(username='labt@example.com', password='asdf1234@')

    def test_prescribed_test_list_logged_in(self):
        """
        Test that the prescribed test list view works when logged in.
        """
        
        response = self.client.get(reverse('medical_tests:test-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_technician/list_of_prescribed_test.html')
        self.assertIn('prescribed_tests', response.context)
        self.assertIn('lab_technician', response.context)


    def test_prescribed_test_list_not_logged_in(self):
        """
        Test that the prescribed test list view redirects to login when not logged in.
        """
        self.client.logout()
        response = self.client.get(reverse('medical_tests:test-list'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, '/users/login/?next=/medical_test/test-list/')


    def test_create_test_report_valid_data(self):
        """
        Test creating a test report with valid data.
        """
        

        # Sample test data
        test_data = {
            'result': 'Normal',
            'attached_file':SimpleUploadedFile("report.pdf", b"file_content", content_type="application/pdf"),
            'notes': 'No issues found.',
        }

        response = self.client.post(
            reverse('medical_tests:create-test-report', args=[self.prescribed_test.id]),
            data=test_data
        )

        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, reverse('medical_tests:test-list'))  # Check if it redirects to the correct view
        self.assertEqual(TestReport.objects.count(), 1)  # Check if a TestReport object was created


    def test_create_test_report_invalid_data(self):
        """
        Test creating a test report with invalid data.
        """
        self.client.login(username='labt@example.com', password='asdf1234@')

        # Sample invalid test data (missing 'result' field)
        invalid_test_data = {
            'notes': 'No issues found.',
        }

        response = self.client.post(
            reverse('medical_tests:create-test-report', args=[self.prescribed_test.id]),
            data=invalid_test_data
        )

        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertTemplateUsed(response, 'lab_technician/create_test_report.html')
        self.assertEqual(TestReport.objects.count(), 0)  # No TestReport object should be created


    def test_see_report_list_logged_in(self):
        """
        Test that the see report list view works when logged in.
        """
        
        response = self.client.get(reverse('medical_tests:see-report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_technician/list_of_report.html')
        self.assertIn('test_reports', response.context)
        self.assertIn('lab_technician', response.context)


    def test_see_report_list_not_logged_in(self):
        """
        Test that the see report list view redirects to login when not logged in.
        """
        self.client.logout()
        response = self.client.get(reverse('medical_tests:see-report-list'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, '/users/login/?next=/medical_test/report-list/')