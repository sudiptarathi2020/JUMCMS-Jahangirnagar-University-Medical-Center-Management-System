from django.contrib import admin

# Register your models here.

from appointments.models import DoctorAppointment

admin.site.register(DoctorAppointment)
