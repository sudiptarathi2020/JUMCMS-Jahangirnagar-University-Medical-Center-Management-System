from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from medicines.models import Prescription, PrescribedMedicine, Medicine
from appointments.models import DoctorAppointment
from users.models import Doctor, Patient
from medical_tests.models import Test
from appointments.controllers import calculate_detailed_age
from medicines.constants import MEDICINE_FREQUENCY_CHOICES


# Doctor part start
@login_required
def get_information_for_prescription(request, appointment_id):
    if request.user.role != "Doctor":
        return HttpResponseForbidden("You are not authorized to view this page.")
    appointment = get_object_or_404(DoctorAppointment, pk=appointment_id)
    patient = get_object_or_404(Patient, pk=appointment.patient.id)
    doctor = get_object_or_404(Doctor, pk=appointment.doctor.id)
    age = calculate_detailed_age(patient.user.date_of_birth)

    tests = Test.objects.all()
    medicines = Medicine.objects.all()
    frequencies = [choice[0] for choice in MEDICINE_FREQUENCY_CHOICES]
    context = {
        "appointment": appointment,
        "doctor": doctor,
        "patient": patient,
        "age": age,
        "medicines": medicines,
        "tests": tests,
        "frequencies": frequencies,
    }
    return render(request, "doctors/prescribe_patient.htm", context)


# Doctor part end
