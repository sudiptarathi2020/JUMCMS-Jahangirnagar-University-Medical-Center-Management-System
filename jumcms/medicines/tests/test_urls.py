from django.test import SimpleTestCase
from django.urls import reverse, resolve
from medicines.controllers import prescription_details, search_prescriptions, all_prescriptions,dispense_medicines

class TestUrls(SimpleTestCase):

    def test_all_prescriptions_url_is_resolved(self):
        """
        Testing of all prescriptions url
        """
        url = reverse('medicines:all_prescriptions')
        self.assertEquals(resolve(url).func, all_prescriptions)

    def test_search_prescriptions_url_is_resolved(self):
        """
        Testing of search prescriptions url
        """
        url = reverse('medicines:search-prescriptions')
        self.assertEquals(resolve(url).func, search_prescriptions)

    def test_prescription_details_url_is_resolved(self):
        """
        Testing of prescription details url
        """
        url = reverse('medicines:prescription-details', args=[1])
        self.assertEquals(resolve(url).func, prescription_details)

    def test_dispense_medicines_url_is_resolved(self):
        """
        Testing of dispense_medicines url
        """
        url = reverse('medicines:dispense-medicines', args=[1])
        self.assertEquals(resolve(url).func, dispense_medicines)