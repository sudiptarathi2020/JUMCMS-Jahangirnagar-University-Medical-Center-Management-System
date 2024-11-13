from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import DoctorAppointment
from django.contrib import messages
from users.models import Patient, Doctor
from datetime import timedelta
from django.utils import timezone
from appointments.forms import DoctorAppointmentCreationForm


# Doctor part start


def get_doctor_appointments(doctor):
    """
    Retrieves all scheduled appointments for a specific doctor.

    This function queries the DoctorAppointment model to fetch appointments that are
    associated with the given doctor and have a status of "scheduled". It returns a
    queryset of these appointments.

    Parameters:
        doctor (Doctor): The Doctor instance for whom the appointments are being retrieved.

    Returns:
        QuerySet: A Django QuerySet containing DoctorAppointment objects with status "scheduled"
                  for the specified doctor.
    """
    appointments = DoctorAppointment.objects.filter(
        doctor=doctor, status="scheduled"
    ).order_by("appointment_date_time")
    return appointments


def delete_doctor_appointment(request, pk):
    """
    Deletes a specific doctor appointment.

    This function retrieves an appointment by its primary key (pk), deletes it, and updates
    the associated doctor's appointment count. It also sends a success message to the user.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the appointment to be deleted.

    Returns:
        HttpResponseRedirect: A redirect to the doctor dashboard after deletion.
    """
    appointment = get_object_or_404(DoctorAppointment, pk=pk)
    doctor = appointment.doctor
    appointment.delete()
    if doctor.no_of_appointments > 0:
        doctor.no_of_appointments -= 1
        doctor.save()
    messages.success(request, "Appointment deleted successfully.")
    return redirect("users:doctor-dashboard")


def get_patient_information(request, pk):
    """
    Retrieves and displays information about a patient associated with a specific appointment.

    This function retrieves the appointment by its primary key (pk) and fetches the related
    patient and doctor information. It also calculates the patient's age and renders a
    template with this information.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the appointment for which patient information is retrieved.

    Returns:
        HttpResponse: A rendered HTML response with patient information.
    """
    appointment = get_object_or_404(DoctorAppointment, pk=pk)
    patient = get_object_or_404(Patient, pk=appointment.patient.id)
    doctor = get_object_or_404(Doctor, pk=appointment.doctor.id)
    age = calculate_detailed_age(patient.user.date_of_birth, timezone.now().date())
    context = {
        "doctor": doctor,
        "patient": patient,
        "age": age,
    }
    return render(request, "doctors/patient_information.htm", context)


def calculate_detailed_age(date_of_birth, date_today):
    today = date_today

    years = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        years -= 1

    months = today.month - date_of_birth.month
    if today.day < date_of_birth.day:
        months -= 1
        if months < 0:
            months += 12

    days = today.day - date_of_birth.day
    if days < 0:
        previous_month = today.replace(day=1) - timedelta(days=1)
        days += previous_month.day

    return f"{years} years, {months} months, {days} days"


# Doctor part end

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
        return redirect("users:users-login")

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
            return redirect("appointments:doctor-appointment-list-for-patient")
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
