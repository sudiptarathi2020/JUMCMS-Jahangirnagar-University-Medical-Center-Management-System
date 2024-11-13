"""
URL configuration for user authentication views.

This module defines the URL patterns for user-related actions such as
registration, login, logout, and handling unapproved users.

URLs:
- /create-account/ : View for user registration.
- /login/ : View for user login.
- /logout/ : View for user logout.
- /unapproved/ : View for handling unapproved users.
- /doctor-dashboard/ : View for Doctor dashboard.
"""

from users.controllers import register, log_in, log_out, unapproved, doctor_dashboard
from django.urls import path
from users.controllers import *

app_name = "users"
urlpatterns = [
    path("create-account/", register, name="users-register"),
    path("login/", log_in, name="users-login"),
    path("logout/", log_out, name="users-logout"),
    path("unapproved/", unapproved, name="unapproved"),
    path("doctor-dashboard/", doctor_dashboard, name="doctor-dashboard"),
    path("patient-dashboard/", patient_dashboard, name="patient-dashboard"),
]
