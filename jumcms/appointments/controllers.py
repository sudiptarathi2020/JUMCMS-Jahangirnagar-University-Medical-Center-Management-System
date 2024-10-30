from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from users.models import Doctor

# Create your views here.


# Doctor part start
@login_required
def get_doctor_appointments(request):
    pass


# Doctor part end
