from django.test import TestCase
from django.urls import reverse
from appointments.models import DoctorAppointment
from users.models import User, Patient, Doctor
from datetime import date, timedelta
from appointments.controllers import get_doctor_appointments, calculate_detailed_age


class DoctorAppointmentControllersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role="patient",
            blood_group="O+",
            date_of_birth="1998-11-02",
            gender="Male",
            phone_number="+8801234567890",
            password="password123",
        )
        self.doctor = Doctor.objects.create(user=self.user, no_of_appointments=0)
        self.patient = Patient.objects.create(user=self.user)
        self.appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=date.today() + timedelta(days=1),
            status="scheduled",
            reason="Routine checkup",
        )

    def test_get_doctor_appointments(self):
        appointments = get_doctor_appointments(self.doctor)
        self.assertIn(self.appointment, appointments)

        # Test with no appointments
        DoctorAppointment.objects.all().delete()
        appointments = get_doctor_appointments(self.doctor)
        self.assertEqual(appointments.count(), 0)

    def test_delete_doctor_appointment(self):
        response = self.client.delete(
            reverse("delete-doctor-appointment", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            DoctorAppointment.objects.filter(pk=self.appointment.pk).exists()
        )

    def test_get_patient_information(self):
        response = self.client.get(
            reverse("patient-information", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctors/patient_information.htm")
        self.assertContains(response, self.patient.user.name)

    def test_calculate_detailed_age(self):
        dob = date(1998, 11, 2)
        expected_age = "25 years, 11 months, 30 days"
        self.assertEqual(calculate_detailed_age(dob), expected_age)

    def test_age_on_birthday_today(self):
        dob = date.today()
        self.assertEqual(calculate_detailed_age(dob), "0 years, 0 months, 0 days")
