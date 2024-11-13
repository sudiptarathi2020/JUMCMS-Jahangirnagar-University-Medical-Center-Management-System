from django.contrib import admin

# Register your models here.
from appointments.models import DoctorAppointment, TestAppointment, Appointment

admin.site.register(TestAppointment)
admin.site.register(DoctorAppointment)

