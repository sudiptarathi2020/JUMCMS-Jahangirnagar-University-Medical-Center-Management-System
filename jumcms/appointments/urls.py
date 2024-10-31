from django.urls import path
from appointments.controllers import test_appointments_list, reschedule_test_appointment

app_name = 'appointments'  # Ensure this matches your app namespace

urlpatterns = [
    path('test_appointment/reschedule/<int:appointment_id>/', reschedule_test_appointment, name='reschedule_test_appointment'),
    path('test_appointments/', test_appointments_list, name='test_appointments_list'),
]
