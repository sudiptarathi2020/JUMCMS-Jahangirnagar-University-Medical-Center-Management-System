# appointments/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import DoctorAppointmentForm
from .models import DoctorAppointment

def create_doctor_appointment(request):
    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("appointments:appointment_list"))
    else:
        form = DoctorAppointmentForm()
    return render(request, "appointments/doctor_appointment.html", {"form": form})

def appointment_list(request):
    appointments = DoctorAppointment.objects.all()
    return render(request, "appointments/list.html", {"appointments": appointments})
