from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from certifications.models import FundraisingRequest
from users.models import User, Patient
User = get_user_model()

class FundraisingRequestTestCase(TestCase):
    def setUp(self):
        """
        Setup
        :return: Object
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

        self.fundraising_request = FundraisingRequest.objects.create(
            patient=self.patient,
            disease_name="Test Disease",
            amount_needed=1000.00,
            details="Test details"
        )
        # Create a client
        self.client.login(username='superuser@example.com', password='asdf1234@')
        
    def test_approve_fundraising_request_toggle(self):
        """Test toggling the approval status and serial number assignment/removal."""
        
        url = reverse('certifications:approve', args=[self.fundraising_request.id])

        # Toggle approval to True
        response = self.client.post(url)
        self.fundraising_request.refresh_from_db()  # Reload from the database
        self.assertTrue(self.fundraising_request.is_approved)
        self.assertIsNotNone(self.fundraising_request.serial_number)
        self.assertEqual(len(self.fundraising_request.serial_number), 20)

        # Toggle approval to False
        response = self.client.post(url)
        self.fundraising_request.refresh_from_db()
        self.assertFalse(self.fundraising_request.is_approved)
        self.assertIsNone(self.fundraising_request.serial_number)

    def test_approve_view_redirect(self):
        """Test that the approve view redirects to the fundraising request list."""
        url = reverse('certifications:approve', args=[self.fundraising_request.id])
        
        response = self.client.post(url)
        self.assertRedirects(response, reverse('certifications:fundraising-request-list'))
    
    def test_message_displayed_on_approval_toggle(self):
        """Test that a success message is displayed after toggling approval status."""
        url = reverse('certifications:approve', args=[self.fundraising_request.id])
        
        response = self.client.post(url, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any("Approval status for" in message.message for message in messages))
