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
from certifications.controllers import *
app_name = 'certifications'
urlpatterns = [
    path("requests/", fundraising_request_list, name="fundraising-request-list"),
    path("approve/<int:request_id>/", approve, name="approve")
]
