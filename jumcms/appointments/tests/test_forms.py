# appointments/tests/test_forms.py
from django.test import TestCase
from appointments.forms import DoctorAppointmentCreationForm
from django.utils import timezone
from users.models import Doctor, User

class DoctorAppointmentCreationFormTest(TestCase):
    def setUp(self):
        # Create test data
        self.doctor_user = User.objects.create_user(
            email='doctor@example.com', name='Dr. Example', role='Doctor',
            blood_group='O+', date_of_birth='1975-08-15', gender='Male',
            phone_number='+8801812345678', password='asdf1234@'
        )
        self.doctor_user.is_approved = True
        self.doctor = Doctor.objects.create(user=self.doctor_user, no_of_appointments=0)
        # Adjust as necessary for your User model

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
        self.assertTrue(form.errors)
