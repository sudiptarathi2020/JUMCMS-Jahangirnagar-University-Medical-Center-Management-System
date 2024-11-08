from django.test import TestCase
from django.urls import reverse
from users.models import Patient, Doctor, User
from appointments.models import DoctorAppointment
from medicines.models import Medicine, Prescription, PrescribedMedicine
from medical_tests.models import Test, PrescribedTest
from datetime import date, timedelta
from medicines.constants import MEDICINE_FREQUENCY_CHOICES
from datetime import datetime, timedelta
from django.contrib import messages


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


class SavePrescriptionTests(TestCase):

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
        self.doctor.no_of_appointments = 1
        self.doctor.save()

    def test_user_is_not_doctor(self):
        self.client.login(email="patientuser@example.com", password="password123")
        response = self.client.post(
            reverse("medicines:save-prescription", args=[self.appointment.id]), {}
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"You are not authorized to view this page.", response.content)

    def test_invalid_appointment_id(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.post(
            reverse("medicines:save-prescription", args=[9999]), {}
        )
        self.assertRedirects(response, reverse("doctor-dashboard"))
        self.assertIn(
            "Invalid appointment",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_successful_prescription_creation(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.post(
            reverse("medicines:save-prescription", args=[self.appointment.id]),
            {
                "complains": "Headache",
                "diagnosis": "Migraine",
                "vital_signs": "Normal",
                "referral": "Neurologist",
                "next_checkup": "",
                "tests": [self.test.id],
                "medicines": [self.medicine.id],
                "durations": [5],
                "instructions": ["Take after meals"],
                "frequencies": ["Morning + Noon"],
            },
        )
        self.assertRedirects(response, reverse("doctor-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "Prescription of Patient User is successfully saved.",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

        prescription = Prescription.objects.first()
        self.assertIsNotNone(prescription)
        self.assertEqual(prescription.complains, "Headache")

        prescribed_medicine = PrescribedMedicine.objects.first()
        self.assertIsNotNone(prescribed_medicine)
        self.assertEqual(prescribed_medicine.medicine.name, "Paracetamol")

        prescribed_test = PrescribedTest.objects.first()
        self.assertIsNotNone(prescribed_test)
        self.assertEqual(prescribed_test.test.name, "CBC")

    def test_invalid_medicine_id(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.post(
            reverse("medicines:save-prescription", args=[self.appointment.id]),
            {
                "complains": "Headache",
                "diagnosis": "Migraine",
                "vital_signs": "Normal",
                "referral": "Neurologist",
                "next_checkup": "",
                "tests": [self.test.id],
                "medicines": [9999],
                "durations": [5],
                "instructions": ["Take after meals"],
                "frequencies": ["Morning + Noon"],
            },
        )
        self.assertRedirects(
            response,
            reverse(
                "medicines:get-information-for-prescription", args=[self.appointment.id]
            ),
        )
        self.assertIn(
            "An error occurred: No Medicine matches the given query.",
            [m.message for m in messages.get_messages(response.wsgi_request)],
        )

    def test_handle_appointment_status_and_doctor_count(self):
        self.client.login(email="doctoruser@example.com", password="password123")
        response = self.client.post(
            reverse("medicines:save-prescription", args=[self.appointment.id]),
            {
                "complains": "Headache",
                "diagnosis": "Migraine",
                "vital_signs": "Normal",
                "referral": "Neurologist",
                "next_checkup": "",
                "tests": [self.test.id],
                "medicines": [self.medicine.id],
                "durations": [5],
                "instructions": ["Take after meals"],
                "frequencies": ["Morning + Noon"],
            },
        )

        self.appointment.refresh_from_db()
        self.doctor_user.refresh_from_db()

        self.assertEqual(self.appointment.status, "completed")
        self.assertEqual(self.appointment.doctor.no_of_appointments, 0)
        self.assertEqual(self.appointment.doctor.no_of_prescriptions, 1)


# Doctor part end
