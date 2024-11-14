from django.contrib import admin
from .models import DoctorAppointment, TestAppointment

admin.site.register(DoctorAppointment)
admin.site.register(TestAppointment)
