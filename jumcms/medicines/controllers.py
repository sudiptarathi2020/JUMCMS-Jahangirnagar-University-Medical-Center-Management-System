from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from medicines.models import Prescription, PrescribedMedicine, Medicine


# Doctor part start
@login_required
def get_information_for_prescription(request, appointment_id):
    pass


# Doctor part end
