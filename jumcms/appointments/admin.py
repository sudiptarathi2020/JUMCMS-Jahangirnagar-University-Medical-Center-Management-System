from django.contrib import admin

# Register your models here.
from appointments.models import Appointment, TestAppointment, DoctorAppointment
admin.site.register(Appointment)
admin.site.register(TestAppointment)
admin.site.register(DoctorAppointment)

