# appointments/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from appointments.forms import DoctorAppointmentForm
from appointments.models import DoctorAppointment
from users.models import Patient

@login_required
def create_doctor_appointment(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "You must be a registered patient to make an appointment.")
        return redirect("appointments:appointment_list")

    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "Doctor appointment created successfully.")
            return redirect("appointments:appointment_list")
    else:
        form = DoctorAppointmentForm()

    return render(request, "appointments/doctor_appointment.html", {"form": form})

@login_required
def appointment_list(request):
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = DoctorAppointment.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        appointments = []  # If the user is not a patient, show an empty list

    return render(request, "appointments/list.html", {"appointments": appointments})
