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

from django.urls import path

from .controllers import register, log_in, log_out, unapproved

urlpatterns = [
    path("create-account/", register, name="users-register"),
    path("login/", log_in, name="users-login"),
    path("logout/", log_out, name="users-logout"),
    path("unapproved/", unapproved, name="unapproved"),
]
