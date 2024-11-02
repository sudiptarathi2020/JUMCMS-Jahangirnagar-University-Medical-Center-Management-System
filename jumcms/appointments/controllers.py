from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from appointments.forms import DoctorAppointmentCreationForm
from appointments.models import DoctorAppointment
from users.models import Patient


# Patient Part Start (Fatima)


@login_required
def create_doctor_appointment(request):
    """
    Handles the creation of a new doctor appointment for a registered patient.

    This view allows a logged-in patient to create a doctor appointment. The view first
    verifies that the user is registered as a patient, ensuring only patients can make
    appointments. If the request is a POST, it processes the form data to create an
    appointment.

    If the form data is valid:
        - It associates the appointment with the current patient.
        - It checks if the patient has any previous appointments with the selected doctor.
          If not, it increments the doctor's `no_of_patients` by one.
        - It increments the doctor’s `no_of_appointments` by one, regardless of whether the
          patient is new to this doctor.
        - The appointment is saved to the database and a success message is displayed.
        - The user is redirected to the list of their appointments.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse:
            - If the request is POST and form submission is successful, redirects to the
              "doctor-appointment-list-for-patient" view.
            - If the request is GET or form submission fails, renders the appointment
              creation form with any validation errors displayed.
    """
    try:
        # Ensure the user is a registered patient
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        # Redirect if the user is not a registered patient
        messages.error(
            request, "You must be a registered patient to make an appointment."
        )
        return redirect("patient-dashboard")

    if request.method == "POST":
        form = DoctorAppointmentCreationForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            # Retrieve the selected doctor and check for existing appointments with the patient
            doctor = form.cleaned_data["doctor"]
            has_existing_appointments = (
                DoctorAppointment.objects.filter(doctor=doctor, patient=patient)
                .exclude(id=appointment.id)
                .exists()
            )

            # Update doctor's patient and appointment counts
            if not has_existing_appointments:
                doctor.no_of_patients += 1
            doctor.no_of_appointments += 1
            doctor.save()

            messages.success(request, "Doctor appointment created successfully.")
            return redirect("doctor-appoinement-list-for-patient")
    else:
        form = DoctorAppointmentCreationForm()

    return render(request, "patients/make_doctor_appointment.html", {"form": form})


@login_required
def get_doctor_appointment_list_for_patient(request):
    """
    Displays a list of all doctor appointments for the logged-in patient.

    This view retrieves and displays all doctor appointments for the currently logged-in
    patient. If the user is not registered as a patient, an empty appointment list will
    be shown. The appointments are rendered in a template, providing the patient with an
    organized view of their scheduled or completed appointments.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered template that displays the list of appointments for
                      the logged-in patient.
                      - If the user is a registered patient, their appointments are
                        shown.
                      - If the user is not registered as a patient, an empty list is shown.
    """
    try:
        # Retrieve appointments for the logged-in patient
        patient = Patient.objects.get(user=request.user)
        appointments = DoctorAppointment.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        # Show an empty list if the user is not a registered patient
        appointments = []

    return render(
        request,
        "patients/doctor_appointment_list.html",
        {"patient": patient, "appointments": appointments},
    )


# Patient Part End (Fatima)
