from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from users.constants import *


class User(AbstractBaseUser):
    phone_number_validator = RegexValidator(
        regex=r"^\+880\d{10}$",
        message="Phone number must start with '+880' and be followed by 10 digits.",
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    role = models.CharField(
        max_length=200,
        choices=ROLE_CHOICES,
    )
    blood_group = models.CharField(
        max_length=200,
        choices=BLOOD_GROUP_CHOICES,
    )
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=200,
        choices=GENDER_CHOICES,
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator],
    )
    profile_picture = models.ImageField(
        upload_to="profilePictures/", default="profilePictures/default.png"
    )
    is_approved = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_appointments = models.IntegerField(default=0)
    qualifications = models.TextField()
    specialty = models.CharField(max_length=100)
    experience_years = models.IntegerField()


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Storekeeper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LabTechnician(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
