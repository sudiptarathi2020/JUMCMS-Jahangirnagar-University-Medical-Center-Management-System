from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from users.constants import *
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(
        self,
        email,
        name,
        role,
        blood_group,
        date_of_birth,
        gender,
        phone_number,
        password=None,
        profile_picture="profile_pictures/default_user.png",
    ):
        """
        Creates and saves a User with the given email, name, role,
        blood group, date of birth, gender, phone number,
        password, and profile picture.

        :param email: User's email address.
        :param name: User's full name.
        :param role: Role of the user (e.g., patient, doctor).
        :param blood_group: Blood group of the user.
        :param date_of_birth: Date of birth of the user.
        :param gender: Gender of the user.
        :param phone_number: User's phone number.
        :param password: User's password.
        :param profile_picture: Path to the user's profile picture.
        :raises ValueError: If no email is provided.
        :return: The created User instance.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            blood_group=blood_group,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            profile_picture=profile_picture,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        name,
        role,
        blood_group,
        date_of_birth,
        gender,
        phone_number,
        password=None,
        profile_picture="profile_pictures/default_user.png",
    ):
        """
        Creates and saves a superuser with the given email, name, role,
        blood group, date of birth, gender, phone number, and password.

        :param email: User's email address.
        :param name: User's full name.
        :param role: Role of the user (must be 'admin' for superusers).
        :param blood_group: Blood group of the user.
        :param date_of_birth: Date of birth of the user.
        :param gender: Gender of the user.
        :param phone_number: User's phone number.
        :param password: User's password.
        :param profile_picture: Path to the user's profile picture.
        :return: The created superuser instance.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            role=role,
            blood_group=blood_group,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            password=password,
            profile_picture=profile_picture,
        )
        user.is_admin = True
        user.is_approved = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom User model that uses email as the username field.
    """

    phone_number_validator = RegexValidator(
        regex=r"^\+880\d{10}$",
        message="Phone number must start with '+880' and be followed by 10 digits.",
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
        help_text="Unique email address for the user.",
    )
    name = models.CharField(max_length=200, help_text="Full name of the user.")
    role = models.CharField(
        max_length=200,
        choices=ROLE_CHOICES,
        help_text="Role of the user (e.g., patient, doctor).",
    )
    blood_group = models.CharField(
        max_length=200,
        choices=BLOOD_GROUP_CHOICES,
        help_text="Blood group of the user.",
    )
    date_of_birth = models.DateField(help_text="Date of birth of the user.")
    gender = models.CharField(
        max_length=200, choices=GENDER_CHOICES, help_text="Gender of the user."
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator],
        help_text="Phone number of the user, in the format '+880XXXXXXXXXX'.",
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default_user.png",
        help_text="Path to the user's profile picture.",
    )
    is_active = models.BooleanField(
        default=True, help_text="Indicates whether the user is active."
    )
    is_approved = models.BooleanField(
        default=False, help_text="Indicates whether the user is approved."
    )
    is_admin = models.BooleanField(
        default=False, help_text="Indicates whether the user is an admin."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the user was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the user was last updated."
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "role",
        "blood_group",
        "date_of_birth",
        "gender",
        "phone_number",
    ]

    def __str__(self):
        """Returns the string representation of the user."""
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission.

        :param perm: The permission name to check.
        :param obj: The object to check the permission against (optional).
        :return: True if the user has the permission, False otherwise.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Checks if the user has permissions to view the app `app_label`.

        :param app_label: The name of the application.
        :return: True if the user has permissions for the app, False otherwise.
        """
        return True

    @property
    def is_staff(self):
        """
        Checks if the user is a member of staff.

        :return: True if the user is an admin, False otherwise.
        """
        return self.is_admin


class Doctor(models.Model):
    """
    Model representing a Doctor, linked to a User.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_appointments = models.IntegerField(
        default=0, help_text="Number of appointments for the doctor."
    )
    no_of_patients = models.IntegerField(
        default=0, help_text="Number of patients consulted with the doctor."
    )
    no_of_prescriptions = models.IntegerField(
        default=0, help_text="Number of prescriptions prepared by the doctor."
    )
    qualifications = models.CharField(
        max_length=200, default="MBBS", help_text="Qualifications of the doctor."
    )
    specialty = models.CharField(
        max_length=100, default="medicine", help_text="Specialty area of the doctor."
    )
    experience_years = models.IntegerField(
        default=0, help_text="Years of experience of the doctor."
    )

    def __str__(self):
        """Returns the string representation of the doctor."""
        return self.user.name


class Patient(models.Model):
    """
    Model representing a Patient, linked to a User.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the string representation of the patient."""
        return self.user.name


class Storekeeper(models.Model):
    """
    Model representing a Storekeeper, linked to a User.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LabTechnician(models.Model):
    """
    Model representing a Lab Technician, linked to a User.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
