from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from medicines.models import Prescription, PrescribedMedicine, Medicine
from medical_tests.models import PrescribedTest
from appointments.models import DoctorAppointment
from users.models import Doctor, Patient
from medical_tests.models import Test
from appointments.controllers import calculate_detailed_age
from medicines.constants import MEDICINE_FREQUENCY_CHOICES
from datetime import datetime, timedelta
from django.utils import timezone

# Doctor part start


@login_required
def get_information_for_prescription(request, appointment_id):
    """
    Retrieve necessary information for creating a prescription.

    Args:
        request: The HTTP request object.
        appointment_id: The ID of the appointment.

    Returns:
        HttpResponseForbidden: If the user is not a doctor.
        HttpResponse: Rendered prescription form with patient, doctor, tests, and medicines.
    """
    if request.user.role != "Doctor":
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Fetch appointment, patient, and doctor details
    appointment = get_object_or_404(DoctorAppointment, pk=appointment_id)
    patient = get_object_or_404(Patient, pk=appointment.patient.id)
    doctor = get_object_or_404(Doctor, pk=appointment.doctor.id)

    # Calculate the patient's detailed age
    age = calculate_detailed_age(patient.user.date_of_birth, timezone.now().date())

    # Fetch all available tests, medicines, and frequency choices
    tests = Test.objects.all()
    medicines = Medicine.objects.all()
    frequencies = [choice[0] for choice in MEDICINE_FREQUENCY_CHOICES]

    # Prepare context for rendering the template
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


@login_required
def save_prescription(request, appointment_id):
    """
    Save a prescription along with prescribed tests and medicines.

    Args:
        request: The HTTP request object containing form data.
        appointment_id: The ID of the appointment.

    Returns:
        HttpResponseForbidden: If the user is not a doctor.
        HttpResponse: Redirect to the doctor dashboard or the prescription form on error.
    """
    if request.user.role != "Doctor":
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Fetch the appointment
    try:
        appointment = DoctorAppointment.objects.get(pk=appointment_id)
    except DoctorAppointment.DoesNotExist:
        messages.error(request, "Invalid appointment")
        return redirect("doctor-dashboard")

    # Collect form data
    complains = request.POST.get("complains")
    diagnosis = request.POST.get("diagnosis")
    vital_signs = request.POST.get("vital_signs")
    referral = request.POST.get("referral")
    next_checkup = request.POST.get("next_checkup") or (
        datetime.now() + timedelta(days=7)
    ).strftime("%Y-%m-%d")
    is_referred = bool(referral)

    # Create a Prescription instance
    try:
        prescription = Prescription.objects.create(
            doctor_appointment=appointment,
            complains=complains,
            diagnosis=diagnosis,
            vitals=vital_signs,
            referrals=referral,
            next_checkup=next_checkup,
            is_referred=is_referred,
        )
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect(
            "medicines:get-information-for-prescription", appointment_id=appointment.id
        )

    # Save prescribed tests
    tests = request.POST.getlist("tests")
    for test_id in tests:
        try:
            test = get_object_or_404(Test, pk=test_id)
            PrescribedTest.objects.create(prescription=prescription, test=test)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(
                "medicines:get-information-for-prescription",
                appointment_id=appointment.id,
            )

    # Save prescribed medicines
    medicines = request.POST.getlist("medicines")
    durations = request.POST.getlist("durations")
    instructions = request.POST.getlist("instructions")
    frequencies = request.POST.getlist("frequencies")

    for index, medicine_id in enumerate(medicines):
        try:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            PrescribedMedicine.objects.create(
                prescription=prescription,
                medicine=medicine,
                duration=durations[index],
                instructions=instructions[index],
                dosage_frequency=frequencies[index],
            )
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(
                "medicines:get-information-for-prescription",
                appointment_id=appointment.id,
            )

    # Update appointment and doctor stats
    appointment.status = "completed"
    appointment.save()
    appointment.doctor.no_of_appointments -= 1
    appointment.doctor.no_of_prescriptions += 1
    appointment.doctor.save()

    messages.success(
        request, f"Prescription for {appointment.patient.user.name} saved successfully."
    )
    return redirect("doctor-dashboard")


# Doctor part end
