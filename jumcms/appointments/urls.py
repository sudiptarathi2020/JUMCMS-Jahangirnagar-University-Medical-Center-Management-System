from django.urls import path
from appointments.controllers import test_appointments_list, test_appointments_fail, reschedule_test_appointment

app_name = 'appointments'  # Ensure this matches your app namespace

urlpatterns = [
    path('appointment/reschedule/<int:appointment_id>/', reschedule_test_appointment, name='reschedule_test_appointment'),
    path('appointments/', test_appointments_list, name='test_appointments_list'),
    path('test-appointments-fail/', test_appointments_fail, name='test_appointments_fail'),
]
