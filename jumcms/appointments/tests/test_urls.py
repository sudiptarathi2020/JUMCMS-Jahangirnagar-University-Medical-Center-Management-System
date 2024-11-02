# appointments/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from appointments.controllers import (
    create_doctor_appointment,
    get_doctor_appointment_list_for_patient,
)

class AppointmentsUrlsTest(SimpleTestCase):
    def test_create_doctor_appointment_url(self):
        url = reverse('appointments:create_doctor_appointment')
        self.assertEqual(url, '/appointments/create/')
        self.assertEqual(resolve(url).func, create_doctor_appointment)

    def test_doctor_appointment_list_for_patient_url(self):
        url = reverse('appointments:doctor-appointment-list-for-patient')
        self.assertEqual(url, '/appointments/doctor-appoinement-list-for-patient/')
        self.assertEqual(resolve(url).func, get_doctor_appointment_list_for_patient)
