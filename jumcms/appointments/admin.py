from django.contrib import admin

# Register your models here.
from appointments.models import DoctorAppointment, TestAppointment

admin.site.register(TestAppointment)
