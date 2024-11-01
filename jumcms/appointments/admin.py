from django.contrib import admin

# Register your models here.
from appointments.models import Appointment, DoctorAppointment, TestAppointment

admin.site.register(DoctorAppointment)
admin.site.register(TestAppointment)