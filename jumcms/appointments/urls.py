"""
URL configuration for the appointments app.

This module contains the URL patterns for the appointments app, mapping 
URL paths to the corresponding view functions.

View Functions
--------------
- `test_appointments_list`: View function to display a list of test appointments.
- `reschedule_test_appointment`: View function to reschedule a specific test appointment.

URL Patterns
------------
- `test_appointment/reschedule/<int:appointment_id>/`: URL for rescheduling a test appointment.
- `test_appointments/`: URL for displaying the list of test appointments.

Namespaces
----------
The `app_name` variable is used to define the namespace for this URL configuration.

Examples
--------
- To access the appointment rescheduling page, use the URL:
  `/test_appointment/reschedule/1/` where `1` is the appointment ID.

- To access the list of test appointments, use the URL:
  `/test_appointments/`.
"""

from django.urls import path

from appointments.controllers import test_appointments_list,reschedule_test_appointment


app_name = 'appointments'  # Ensure this matches your app namespace

urlpatterns = [
    path(
        'test_appointment/reschedule/<int:appointment_id>/',
        reschedule_test_appointment,
        name='reschedule_test_appointment'
    ),
    path(
        'test_appointments/',
        test_appointments_list,
        name='test_appointments_list'
    ),
]
