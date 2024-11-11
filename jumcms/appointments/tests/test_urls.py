from django.test import SimpleTestCase
from django.urls import reverse, resolve
from appointments.controllers import (
    test_appointments_list,
    reschedule_test_appointment,
)

class AppointmentsUrlsTestCase(SimpleTestCase):
    """
    Class for testing urls.py in appointments app
    """
    def test_reschedule_test_appointment_url_is_resolved(self):
        """
        Testing reschedule test appointment urls
        """
        url = reverse('appointments:reschedule_test_appointment', args=[1]) 
        self.assertEqual(resolve(url).func, reschedule_test_appointment)

    def test_test_appointments_list_url_is_resolved(self):
        """
        Testing the test appointments urls 
        """
        url = reverse('appointments:test_appointments_list')
        self.assertEqual(resolve(url).func, test_appointments_list)
        
    