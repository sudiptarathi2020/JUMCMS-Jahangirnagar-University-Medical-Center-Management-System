from django.test import TestCase
from ambulance.models import Ambulance

class AmbulanceModelTest(TestCase):

    def test_ambulance_creation(self):
        ambulance = Ambulance.objects.create(
            registration_number="TEST-123",
            driver_name="John Doe",
            contact_number="1234567890",
            current_location="Some Location",
            latitude=23.8103,  # Example latitude
            longitude=90.4125,  # Example longitude
        )
        self.assertEqual(str(ambulance), "Ambulance TEST-123")
        self.assertEqual(ambulance.driver_name, "John Doe")
        self.assertTrue(ambulance.is_available)  # Default value