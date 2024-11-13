"""
URL configuration for user authentication views.

This module defines the URL patterns for user-related actions such as 
registration, login, logout, and handling unapproved users.

URLs:
- /create-account/ : View for user registration.
- /login/ : View for user login.
- /logout/ : View for user logout.
- /unapproved/ : View for handling unapproved users.
"""

from django.urls import path, include
from users.controllers import *
app_name = 'users'
urlpatterns = [
    path("create-account/", register, name="users-register"),
    path("login/", log_in, name="users-login"),
    path("logout/", log_out, name="users-logout"),
    path("unapproved/", unapproved, name="unapproved"),
    path("doctor_dashboard/", doctor_dashboard, name="doctor_dashboard"),
    path("storekeeper-dashboard/", storekeeper_dashboard, name="storekeeper_dashboard"),
    path("lab_technician_dashboard/", lab_technician_dashboard, name="lab_technician_dashboard"),
    path('ambulance-info/', ambulance_info, name='ambulance_info'),
]
