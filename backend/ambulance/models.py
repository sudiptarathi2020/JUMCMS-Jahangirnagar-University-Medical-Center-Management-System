from django.db import models

class Ambulance(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    driver_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    current_location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)  # Allow null values initially
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Ambulance {self.registration_number}"