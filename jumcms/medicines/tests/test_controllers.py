from datetime import timedelta, date
from unittest.mock import patch

from django.contrib import messages
from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from appointments.models import DoctorAppointment
from medical_tests.models import Test, PrescribedTest
from medicines.constants import MEDICINE_FREQUENCY_CHOICES
from medicines.models import Medicine, Prescription, PrescribedMedicine
from users.models import Patient, Doctor, User


class StorekeeperControllerTest(TestCase):
    """
    StroreKeeperControllerTest
    """

    def setUp(self):
        """
        Setup
        :return: Object
        """
        Medicine.objects.all().delete()
        Prescription.objects.all().delete()
        PrescribedMedicine.objects.all().delete()
        DoctorAppointment.objects.all().delete()
        User.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        self.storekeeper_user = User.objects.create_user(
            email="storekeeper@example.com",
            name="Storekeeper",
            role="Storekeeper",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            password="asdf1234@",
        )
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Sudipta",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            password="asdf1234@",
        )
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            password="asdf1234@",
        )

        # Create doctor and patient instances
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(user=self.patient_user)

        # Create appointment
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date_time="2024-12-15T10:00:00Z",
            status="scheduled",
        )

        # Create medicine
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            generic_name="Acetaminophen",
            manufacturer="ABC Pharma",
            dosage_form="Tablet",
            strength="500mg",
            description="Pain reliever",
            price=10.00,
            stock_quantity=100,
            expiry_date="2025-12-31",
        )

        # Create prescription and prescribed medicine
        self.prescription = Prescription.objects.create(
            doctor_appointment=self.appointment,
            diagnosis="Headache",
            next_checkup="2024-12-22",
        )
        self.prescribed_medicine = PrescribedMedicine.objects.create(
            prescription=self.prescription,
            medicine=self.medicine,
            dosage_frequency=MEDICINE_FREQUENCY_CHOICES[0][0],
            duration=5,
            instructions="Take after meal",
        )

        # Create a client
        self.client = Client()

    def test_all_prescriptions_controllers(self):
        """
        All Prescriptions
        :return: Boolean
        """
        self.client.force_login(self.storekeeper_user)
        response = self.client.get(reverse("medicines:all_prescriptions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "storekeeper/prescription_list.html")
        self.assertIn("prescriptions", response.context)

    def test_search_prescriptions_view_get(self):
        """
        test_search_prescriptions_view_get
        :return: Boolean
        """
        self.client.force_login(self.storekeeper_user)
        response = self.client.get(reverse("medicines:search-prescriptions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "storekeeper/prescription_search.html")

    def test_search_prescriptions_view_post(self):
        """
        Test search_prescriptions_view_post
        :return:  Boolean
        """
        self.client.force_login(self.storekeeper_user)
        response = self.client.post(
            reverse("medicines:search-prescriptions"), {"patient_name": "John"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "storekeeper/prescription_list.html")
        self.assertIn("prescriptions", response.context)
        self.assertEqual(len(response.context["prescriptions"]), 1)

    def test_prescription_details_view(self):
        """
        test_prescription_details_view
        :return: Boolean
        """
        self.client.force_login(self.storekeeper_user)
        response = self.client.get(
            reverse("medicines:prescription-details", args=[self.prescription.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "storekeeper/prescribed_medicine_details.html"
        )
        self.assertIn("prescription", response.context)
        self.assertIn("medicines_info", response.context)

    @patch("medicines.controllers.generate_pdf")  # Mock the generate_pdf function
    def test_dispense_medicines_view_success(self, mock_generate_pdf):
        """
        Test dispense_medicines_view_success
        :param mock_generate_pdf:
        :return:
        """
        mock_generate_pdf.return_value = HttpResponse()  # Mock the return value

        self.client.force_login(self.storekeeper_user)
        response = self.client.post(
            reverse("medicines:dispense-medicines", args=[self.prescription.id])
        )

        # Assert that the medicine stock quantity is updated
        updated_medicine = Medicine.objects.get(id=self.medicine.id)
        self.assertEqual(updated_medicine.stock_quantity, 95)

        # Assert that the response is a redirect (since generate_pdf is mocked)
        self.assertEqual(response.status_code, 200)

    def test_dispense_medicines_view_not_enough_stock(self):
        """
        test dispense medicines view_not_enough_stock
        :return: Boolean
        """
        self.client.force_login(self.storekeeper_user)
        self.medicine.stock_quantity = 2
        self.medicine.save()
        response = self.client.post(
            reverse("medicines:dispense-medicines", args=[self.prescription.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("medicines:search-prescriptions"))

    def test_add_medicine_controller(self):
        """
        Test add_medicine_controller

        """
        self.client.force_login(self.storekeeper_user)
        self.assertEqual(Medicine.objects.count(), 1)
        response = self.client.post(
            reverse("medicines:add-medicine"),
            {
                "name": "Capa",
                "generic_name": "Maracetamol",
                "manufacturer": "Square",
                "dosage_form": "Tablet",
                "strength": "200mg",
                "description": "Used for fever",
                "price": 10.00,
                "stock_quantity": 100,
                "expiry_date": "2025-12-31",
            },
            follow=False,
        )
        self.assertRedirects(response, reverse("users:storekeeper_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Medicine.objects.count(), 2)
        self.assertEqual(Medicine.objects.first().name, "Paracetamol")
        self.assertEqual(Medicine.objects.first().generic_name, "Acetaminophen")
        self.assertEqual(Medicine.objects.first().manufacturer, "ABC Pharma")
        self.assertEqual(Medicine.objects.first().dosage_form, "Tablet")
        self.assertEqual(Medicine.objects.first().strength, "500mg")
        self.assertEqual(Medicine.objects.first().description, "Pain reliever")
        self.assertEqual(Medicine.objects.first().price, 10.00)
        self.assertEqual(Medicine.objects.first().stock_quantity, 100)
        self.assertEqual(str(Medicine.objects.first().expiry_date), "2025-12-31")


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
            appointment_date_time=timezone.now() + timedelta(days=1),
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
            appointment_date_time=timezone.now() + timedelta(days=1),
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
        self.assertRedirects(response, reverse("users:doctor-dashboard"))
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
        self.assertRedirects(response, reverse("users:doctor-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "Prescription for Patient User saved successfully.",
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
