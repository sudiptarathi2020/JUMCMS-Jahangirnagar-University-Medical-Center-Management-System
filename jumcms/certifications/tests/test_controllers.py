from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from certifications.models import FundraisingRequest
from users.models import User, Patient
from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()

class FundraisingRequestTestCase(TestCase):
    """
    Test case for FundraisingRequest model functionality, including toggling 
    approval status, checking serial number assignment, and attachment handling.
    """
    def setUp(self):
        """
        Sets up the initial test data including admin user, patient user, patient, 
        and a sample FundraisingRequest instance with an attachment.
        
        Creates:
            - An admin user for performing actions in the test case.
            - A patient user and associated Patient instance for the fundraising request.
            - A sample file to act as an attachment for the fundraising request.
            - A FundraisingRequest instance linked to the patient.
        """
        self.adminuser = User.objects.create_superuser(
            email='superuser@example.com', name='super', role='Admin',
            blood_group='A+', date_of_birth='1980-01-01', gender='Male',
            phone_number='+8801712345678', password='asdf1234@'
        )
        self.patient_user = User.objects.create_user(
            email='patient@example.com', name='John Doe', role='Student',
            blood_group='B+', date_of_birth='1990-05-10', gender='Male',
            phone_number='+8801987654321', password='asdf1234@'
        )
        self.patient = Patient.objects.create(user=self.patient_user)
        self.attachment = SimpleUploadedFile("test_attachment.txt", b"Sample content for testing.")

        self.fundraising_request = FundraisingRequest.objects.create(
            patient=self.patient,
            disease_name="Test Disease",
            amount_needed=1000.00,
            attachments=self.attachment,
            details="Test details"
        )
        
        # Create a client
        self.client.login(username='superuser@example.com', password='asdf1234@')

    def test_approve_fundraising_request_toggle(self):
        """
        Tests toggling the approval status of a fundraising request and validates 
        serial number assignment and attachment presence.

        Steps:
            - Sends a POST request to toggle approval status to True.
            - Verifies that the request is approved, a serial number is generated, 
              and the attachment is present.
            - Sends another POST request to toggle approval status to False.
            - Verifies that approval is removed and the serial number is set to None.
        """
        
        url = reverse('certifications:approve', args=[self.fundraising_request.id])

        # Toggle approval to True
        response = self.client.post(url)
        self.fundraising_request.refresh_from_db()  # Reload from the database
        self.assertTrue(self.fundraising_request.is_approved)
        self.assertIsNotNone(self.fundraising_request.serial_number)
        self.assertEqual(len(self.fundraising_request.serial_number), 20)
        self.assertTrue(bool(self.fundraising_request.attachments))
        self.assertTrue(FundraisingRequest.objects.count(),1)

        # Toggle approval to False
        response = self.client.post(url)
        self.fundraising_request.refresh_from_db()
        self.assertFalse(self.fundraising_request.is_approved)
        self.assertIsNone(self.fundraising_request.serial_number)

    def test_approve_view_redirect(self):
        """
        Tests that the approve view correctly redirects to the fundraising 
        request list after toggling approval status.
        
        Verifies:
            - Redirects to the 'fundraising-request-list' page after the POST request.
        """
        url = reverse('certifications:approve', args=[self.fundraising_request.id])
        
        response = self.client.post(url)
        self.assertRedirects(response, reverse('certifications:fundraising-request-list'))
    
    def test_message_displayed_on_approval_toggle(self):
        """
        Tests that a success message is displayed after toggling the approval 
        status of the fundraising request.
        
        Verifies:
            - Checks if any message contains "Approval status for" after the action.
        """
        url = reverse('certifications:approve', args=[self.fundraising_request.id])
        
        response = self.client.post(url, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any("Approval status for" in message.message for message in messages))
