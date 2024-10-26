from django.urls import path

from .controllers import register, log_in, log_out

urlpatterns = [
    path("create-account/", register, name="users-register"),
    path("login/", log_in, name="users-login"),
    path("logout/", log_out, name="users-logout"),
]
