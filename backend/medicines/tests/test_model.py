from django.test import TestCase
from medicines.models import Medicine, Prescription, PrescribedMedicine
from appointments.models import DoctorAppointment
from users.models import User, Doctor, Patient
from medicines.constants import MEDICINE_FREQUENCY_CHOICES


class MedicineModelTest(TestCase):
    """
    Medicine model tests
    """

    def test_medicine_str(self):
        """
        test_medicine_str
        :return: Boolean
        """
        medicine = Medicine.objects.create(
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
        self.assertEqual(str(medicine), "Paracetamol (500mg)")

    def test_medicine_fields(self):
        """
        test_medicine_fields
        :return: Boolean
        """
        medicine = Medicine.objects.create(
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
        self.assertEqual(medicine.name, "Paracetamol")
        self.assertEqual(medicine.generic_name, "Acetaminophen")
        self.assertEqual(medicine.manufacturer, "ABC Pharma")
        self.assertEqual(medicine.dosage_form, "Tablet")
        self.assertEqual(medicine.strength, "500mg")
        self.assertEqual(medicine.description, "Pain reliever")
        self.assertEqual(medicine.price, 10.00)
        self.assertEqual(medicine.stock_quantity, 100)
        self.assertEqual(medicine.expiry_date, "2025-12-31")


class PrescriptionModelTest(TestCase):
    """
    Prescription model tests
    """

    def setUp(self):
        """
        Setup
        :return: objects
        """
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Sudipta",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            role_id = "asdf1234",
            password="asdf1234@",
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            role_id= "asdf124456A",
            password="asdf1234@",
        )
        self.patient = Patient.objects.create(user=self.patient_user)
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date_time="2024-12-15T10:00:00Z",
            status="completed",
        )

    def test_prescription_str(self):
        """
        test_prescription_str
        :return: Boolean
        """
        prescription = Prescription.objects.create(
            doctor_appointment=self.appointment,
            diagnosis="Headache",
            next_checkup="2024-12-22",
        )
        expected_str = f"Prescription for {self.patient_user.name} by {self.doctor_user.name} on {prescription.date_issued}"
        self.assertEqual(str(prescription), expected_str)

    def test_prescription_fields(self):
        """
        test_prescription_fields
        :return: Boolean
        """
        prescription = Prescription.objects.create(
            doctor_appointment=self.appointment,
            diagnosis="Headache",
            next_checkup="2024-12-22",
        )
        self.assertEqual(prescription.doctor_appointment, self.appointment)
        self.assertEqual(prescription.diagnosis, "Headache")
        self.assertEqual(prescription.next_checkup, "2024-12-22")


class PrescribedMedicineModelTest(TestCase):
    """
    Prescribed Medicine model tests
    """

    def setUp(self):
        """
        Setup of  test
        :return: objects
        """
        self.doctor_user = User.objects.create_user(
            email="doctor@example.com",
            name="Dr. Sudipta",
            role="Doctor",
            blood_group="A+",
            date_of_birth="1980-01-01",
            gender="Male",
            phone_number="+8801712345678",
            role_id = "hghghkh",
            password="asdf1234@",
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient_user = User.objects.create_user(
            email="patient@example.com",
            name="John Doe",
            role="Student",
            blood_group="B+",
            date_of_birth="1990-05-10",
            gender="Male",
            phone_number="+8801987654321",
            role_id = "hhhgkkkk",
            password="asdf1234@",
        )
        self.patient = Patient.objects.create(user=self.patient_user)
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date_time="2024-12-15T10:00:00Z",
            status="scheduled",
        )
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
        self.prescription = Prescription.objects.create(
            doctor_appointment=self.appointment,  # Use the appointment from setUp
            diagnosis="Headache",
            next_checkup="2024-12-22",
        )

    def test_prescribed_medicine_str(self):
        """
        test_prescribed medicine
        :return:
        """
        prescribed_medicine = PrescribedMedicine.objects.create(
            prescription=self.prescription,
            medicine=self.medicine,
            dosage_frequency=MEDICINE_FREQUENCY_CHOICES[0][
                0
            ],  # Choose a frequency from your choices
            duration=5,
            instructions="Take after meal",
        )
        expected_str = f"{self.medicine.name} for {self.patient_user.name}"
        self.assertEqual(str(prescribed_medicine), expected_str)

    def test_prescribed_medicine_fields(self):
        """
        test_prescribed_medicine
        :return: boolean
        """
        prescribed_medicine = PrescribedMedicine.objects.create(
            prescription=self.prescription,
            medicine=self.medicine,
            dosage_frequency=MEDICINE_FREQUENCY_CHOICES[0][0],
            duration=5,
            instructions="Take after meal",
        )
        self.assertEqual(prescribed_medicine.prescription, self.prescription)
        self.assertEqual(prescribed_medicine.medicine, self.medicine)
        self.assertEqual(
            prescribed_medicine.dosage_frequency, MEDICINE_FREQUENCY_CHOICES[0][0]
        )
        self.assertEqual(prescribed_medicine.duration, 5)
        self.assertEqual(prescribed_medicine.instructions, "Take after meal")
