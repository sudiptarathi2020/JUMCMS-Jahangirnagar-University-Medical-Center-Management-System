from django.test import TestCase
from django.urls import reverse
from users.models import Patient, Doctor, User
from appointments.models import DoctorAppointment
from medicines.models import Medicine
from medical_tests.models import Test
from datetime import date, timedelta
from medicines.constants import MEDICINE_FREQUENCY_CHOICES


# Doctor part start
class GetInformationForPrescriptionTests(TestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            email="doctoruser@example.com",
            name="Doctor User",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1990-01-01",
            gender="Male",
            phone_number="+8801234567890",
            password="password123",
        )
        self.patient_user = User.objects.create_user(
            email="patientuser@example.com",
            name="Patient User",
            role="Patient",
            blood_group="A+",
            date_of_birth="1990-01-01",
            gender="Female",
            phone_number="+8801234567890",
            password="password123",
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(user=self.patient_user)
        self.appointment = DoctorAppointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date_time=date.today() + timedelta(days=1),
            status="scheduled",
            reason="Routine checkup",
        )
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            generic_name="Acetaminophen",
            manufacturer="Pharma Co.",
            dosage_form="Tablet",
            strength="500mg",
            description="Used for relieving pain and fever.",
            price=20.50,
            stock_quantity=100,
            expiry_date=date(2025, 12, 31),
        )
        self.test = Test.objects.create(
            name="CBC",
            description="Blood test",
            department="Hematology",
            is_available=True,
        )

    def test_valid_appointment(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        url = reverse(
            "medicines:get-information-for-prescription", args=[self.appointment.id]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("appointment", response.context)
        self.assertIn("doctor", response.context)
        self.assertIn("patient", response.context)
        self.assertIn("age", response.context)

    def test_appointment_not_found(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        url = reverse("medicines:get-information-for-prescription", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_not_logged_in(self):
        url = reverse(
            "medicines:get-information-for-prescription", args=[self.appointment.id]
        )
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_context_data(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.get(
            reverse(
                "medicines:get-information-for-prescription", args=[self.appointment.id]
            )
        )
        self.assertEqual(response.context["appointment"], self.appointment)
        self.assertEqual(response.context["doctor"], self.doctor)
        self.assertEqual(response.context["patient"], self.patient)
        self.assertIn(self.medicine, response.context["medicines"])
        self.assertIn(self.test, response.context["tests"])
        self.assertListEqual(
            response.context["frequencies"],
            [choice[0] for choice in MEDICINE_FREQUENCY_CHOICES],
        )

    def test_correct_template_used(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.get(
            reverse(
                "medicines:get-information-for-prescription", args=[self.appointment.id]
            )
        )
        self.assertTemplateUsed(response, "doctors/prescribe_patient.htm")

    def test_no_medicines_or_tests(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        Medicine.objects.all().delete()
        Test.objects.all().delete()
        url = reverse(
            "medicines:get-information-for-prescription", args=[self.appointment.id]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("medicines", response.context)
        self.assertIn("tests", response.context)
        self.assertEqual(len(response.context["medicines"]), 0)
        self.assertEqual(len(response.context["tests"]), 0)


# Doctor part end
