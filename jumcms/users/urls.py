from django.urls import path

from .controllers import register, login, logout

urlpatterns = [
    path("create-account/", register, name="users-register"),
    path("login/", login, name="users-login"),
    path("logout/", logout, name="users-logout"),
]
