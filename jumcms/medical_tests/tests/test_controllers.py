from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from appointments.models import DoctorAppointment
from medical_tests.models import PrescribedTest, TestReport, Test
from medicines.models import Prescription
from users.models import Patient, User, Doctor, LabTechnician


class LabTechnicianControllersTest(TestCase):
    def setUp(self):
        # Create a test user (Lab Technician)
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Sudipta",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            password="asdf1234@",
        )
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            password="asdf1234@",
        )

        self.lab_technician_user = User.objects.create_user(
            email="labt@example.com",
            name="lab technician",
            role="Lab_technician",
            blood_group="A+",
            date_of_birth="2000-04-04",
            gender="Male",
            phone_number="+8801711111111",
            password="asdf1234@",
        )
        self.lab_technician = LabTechnician.objects.create(
            user=self.lab_technician_user
        )
        # Create doctor and patient instances
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(user=self.patient_user)

        self.doctor_appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time="2000-05-05T10:10:10Z",
        )

        # Create a test patient, doctor, and prescription
        self.prescription = Prescription.objects.create(
            doctor_appointment=self.doctor_appointment,
            date_issued=timezone.now(),
            diagnosis="HEPA",
        )
        self.test = Test.objects.create(name="CBC", description="cancer'")
        # Create a test prescribed test
        self.prescribed_test = PrescribedTest.objects.create(
            prescription=self.prescription,
            test=self.test,
        )

        # Create a test client
        self.client = Client()
        self.client.login(username="labt@example.com", password="asdf1234@")

    def test_prescribed_test_list_logged_in(self):
        """
        Test that the prescribed test list view works when logged in.
        """

        response = self.client.get(reverse("medical_tests:test-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lab_technician/list_of_prescribed_test.html")
        self.assertIn("prescribed_tests", response.context)
        self.assertIn("lab_technician", response.context)

    def test_prescribed_test_list_not_logged_in(self):
        """
        Test that the prescribed test list view redirects to login when not logged in.
        """
        self.client.logout()
        response = self.client.get(reverse("medical_tests:test-list"))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, "/accounts/login/?next=/medical_test/test-list/")

    def test_create_test_report_valid_data(self):
        """
        Test creating a test report with valid data.
        """

        # Sample test data
        test_data = {
            "result": "Normal",
            "attached_file": SimpleUploadedFile(
                "report.pdf", b"file_content", content_type="application/pdf"
            ),
            "notes": "No issues found.",
        }

        response = self.client.post(
            reverse("medical_tests:create-test-report", args=[self.prescribed_test.id]),
            data=test_data,
        )

        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertRedirects(
            response, reverse("medical_tests:see-report-list")
        )  # Check if it redirects to the correct view
        self.assertEqual(
            TestReport.objects.count(), 1
        )  # Check if a TestReport object was created

    def test_create_test_report_invalid_data(self):
        """
        Test creating a test report with invalid data.
        """
        self.client.login(username="labt@example.com", password="asdf1234@")

        # Sample invalid test data (missing 'result' field)
        invalid_test_data = {
            "notes": "No issues found.",
        }
        with self.assertLogs('root', level='ERROR') as log_capture:
            response = self.client.post(
                reverse('medical_tests:create-test-report', args=[self.prescribed_test.id]),
                data=invalid_test_data
            )

            # Check response status code
            self.assertEqual(response.status_code, 200)

            # Check the template used
            self.assertTemplateUsed(response, 'lab_technician/create_test_report.html')

            # Verify form error for missing required field
            self.assertFormError(response, 'form', 'result', 'This field is required.')

            # Check that an error log was created for the invalid form
            self.assertTrue(
                any("Form is not valid" in message for message in log_capture.output),
                "Expected error log message not found."
            )
            self.assertEqual(
                TestReport.objects.count(), 0
            )  # No TestReport object should be created

    def test_see_report_list_logged_in(self):
        """
        Test that the see report list view works when logged in.
        """

        response = self.client.get(reverse("medical_tests:see-report-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lab_technician/list_of_report.html")
        self.assertIn("test_reports", response.context)
        self.assertIn("lab_technician", response.context)

    def test_see_report_list_not_logged_in(self):
        """
        Test that the see report list view redirects to login when not logged in.
        """
        self.client.logout()
        response = self.client.get(reverse("medical_tests:see-report-list"))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(
            response, "/accounts/login/?next=/medical_test/report-list/"
        )


class TestReportViewTests(TestCase):
    """Test suite for views related to viewing and downloading test reports."""

    def setUp(self):
        """Set up the necessary objects for testing TestReport-related views, including users, patient, doctor, and test report."""
        # Create a user and patient
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            password="asdf1234@",
        )
        self.patient_user.set_password = "asdf1234@"
        self.patient_user.save()
        self.patient = Patient.objects.create(user=self.patient_user)
        # Create related objects for the test report

        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Doctor",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1999-05-10",
            gender="Male",
            phone_number="+8801711111111",
            password="asdf1234@",
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date_time="2024-12-15T10:00:00Z",
            status="scheduled",
        )
        self.prescription = Prescription.objects.create(
            doctor_appointment=self.appointment,
            complains="Fever",
            vitals="Very Bad",
            diagnosis="Good",
        )
        self.test = Test.objects.create(
            name="Blood Test", description="Complete blood count"
        )
        self.prescribed_test = PrescribedTest.objects.create(
            prescription=self.prescription, test=self.test
        )
        self.test_report = TestReport.objects.create(
            prescribed_test=self.prescribed_test, result="Cancer", notes="Die"
        )

        self.client = Client()
        self.client.login(username="patient@example.com", password="asdf1234@")

    def test_view_test_report_authenticated(self):
        """Test that authenticated users can access the view_test_report view."""
        self.client.login(username="patient@example.com", password="asdf1234@")
        response = self.client.get(reverse("medical_tests:view-test-report"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patients/view_test_report.html")
        self.assertIn(self.test_report, response.context["reports"])

    def test_view_test_report_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse("medical_tests:view-test-report"))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(
            response, "/accounts/login/?next=/medical_test/view_test_report/"
        )

    def test_download_test_report_authenticated(self):
        """Test that authenticated users can download a test report."""
        self.client.login(username="patient@example.com", password="asdf1234@")
        response = self.client.get(
            reverse("medical_tests:download-test-report", args=[self.test_report.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/pdf")
        self.assertIn(
            'attachment; filename="TestReport_', response["Content-Disposition"]
        )

    def test_download_test_report_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(
            reverse("medical_tests:download-test-report", args=[self.test_report.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/medical_test/Download_test_report/{self.test_report.id}/",
        )

    def test_download_test_report_invalid_id(self):
        """Test that accessing an invalid report ID returns a 404."""
        invalid_report_id = 999
        response = self.client.get(
            reverse("medical_tests:download-test-report", args=[invalid_report_id])
        )
        self.assertEqual(response.status_code, 404)
