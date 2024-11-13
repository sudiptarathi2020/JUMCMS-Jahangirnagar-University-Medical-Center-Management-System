# appointments/tests/test_forms.py

from django.test import TestCase
from appointments.forms import DoctorAppointmentCreationForm
from django.utils import timezone
from users.models import Doctor

class DoctorAppointmentCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data
        cls.doctor = Doctor.objects.create(user_id=1)  # Adjust as necessary for your User model

    def test_valid_form(self):
        # Test case for valid form submission
        data = {
            'doctor': self.doctor.id,
            'appointment_date_time': timezone.now() + timezone.timedelta(days=1),
            'reason': 'Regular check-up',
            'is_emergency': False,
        }
        form = DoctorAppointmentCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        # Test case for missing required fields
        form = DoctorAppointmentCreationForm(data={})  # No data
        self.assertFalse(form.is_valid())
        self.assertIn('doctor', form.errors)
        self.assertIn('appointment_date_time', form.errors)
        self.assertIn('reason', form.errors)
