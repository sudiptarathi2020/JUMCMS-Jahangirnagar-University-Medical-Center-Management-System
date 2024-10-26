from django.urls import path

from .controllers import register, log_in, logout

urlpatterns = [
    path('register/', register, name='users-register'),
    path('login/', log_in, name='users-login'),
    path('logout/', logout, name='users-logout'),
]