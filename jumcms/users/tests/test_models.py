from django.test import TestCase
from django.utils import timezone
from users.models import User, Doctor, Patient, Storekeeper, LabTechnician
from users.constants import ROLE_CHOICES, BLOOD_GROUP_CHOICES, GENDER_CHOICES


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            role=ROLE_CHOICES[0][0],
            blood_group=BLOOD_GROUP_CHOICES[0][0],
            date_of_birth=timezone.now().date(),
            gender=GENDER_CHOICES[0][0],
            phone_number="+8801234567890",
            role_id="asdf12",
            password="password123",
        )

    def test_user_creation(self):
        """Test creating a user."""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.name, "Test User")
        self.assertTrue(self.user.check_password("password123"))
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_approved)

    def test_user_str(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_user_has_perm(self):
        """Test user permission checking."""
        self.assertFalse(self.user.has_perm("some_permission"))

    def test_user_is_staff(self):
        """Test if user is staff."""
        self.assertFalse(self.user.is_staff)


class DoctorModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="doctor@example.com",
            name="Doctor Who",
            role=ROLE_CHOICES[1][0],  # Assuming this is the Doctor role
            blood_group=BLOOD_GROUP_CHOICES[0][0],
            date_of_birth=timezone.now().date(),
            gender=GENDER_CHOICES[0][0],
            phone_number="+8801234567890",
            role_id = "asdf123",
            password="password123",
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            no_of_appointments=10,
            qualifications="MBBS, MD",
            specialty="Cardiology",
            experience_years=5,
        )

    def test_doctor_creation(self):
        """Test creating a doctor."""
        self.assertEqual(self.doctor.user.email, "doctor@example.com")
        self.assertEqual(self.doctor.no_of_appointments, 10)
        self.assertEqual(self.doctor.qualifications, "MBBS, MD")
        self.assertEqual(self.doctor.specialty, "Cardiology")
        self.assertEqual(self.doctor.experience_years, 5)


class PatientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="patient@example.com",
            name="Patient Smith",
            role=ROLE_CHOICES[2][0],  # Assuming this is the Patient role
            blood_group=BLOOD_GROUP_CHOICES[0][0],
            date_of_birth=timezone.now().date(),
            gender=GENDER_CHOICES[0][0],
            phone_number="+8801234567890",
            role_id = "asdf12345",
            password="password123",
        )
        self.patient = Patient.objects.create(user=self.user)

    def test_patient_creation(self):
        """Test creating a patient."""
        self.assertEqual(self.patient.user.email, "patient@example.com")


class StorekeeperModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="storekeeper@example.com",
            name="Storekeeper Jones",
            role=ROLE_CHOICES[3][0],
            blood_group=BLOOD_GROUP_CHOICES[0][0],
            date_of_birth=timezone.now().date(),
            gender=GENDER_CHOICES[0][0],
            phone_number="+8801234567890",
            role_id = "asdf123456A",
            password="password123",
        )
        self.storekeeper = Storekeeper.objects.create(user=self.user)

    def test_storekeeper_creation(self):
        """Test creating a storekeeper."""
        self.assertEqual(self.storekeeper.user.email, "storekeeper@example.com")


class LabTechnicianModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="labtech@example.com",
            name="Lab Tech",
            role=ROLE_CHOICES[4][0],  # Assuming this is the Lab Technician role
            blood_group=BLOOD_GROUP_CHOICES[0][0],
            date_of_birth=timezone.now().date(),
            gender=GENDER_CHOICES[0][0],
            phone_number="+8801234567890",
            role_id = "asdf123456B",
            password="password123",
        )
        self.lab_technician = LabTechnician.objects.create(user=self.user)

    def test_lab_technician_creation(self):
        """Test creating a lab technician."""
        self.assertEqual(self.lab_technician.user.email, "labtech@example.com")
