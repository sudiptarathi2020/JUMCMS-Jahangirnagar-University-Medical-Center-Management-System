# appointments/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from appointments.forms import DoctorAppointmentForm
from appointments.models import DoctorAppointment
from users.models import Patient

# Patient Part Start (Fatima)
@login_required
def create_doctor_appointment(request):
    """
    Handles the creation of a new doctor appointment for a registered patient.
    This view requires the user to be logged in and registered as a patient. If the 
    request method is POST, it processes the submitted form. If the form is valid, 
    it associates the appointment with the current patient and saves it. 

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A redirect to the appointment list on successful creation or 
                       renders the appointment creation form with error messages.
    """

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "You must be a registered patient to make an appointment.")
        return redirect("appointment_list")

    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "Doctor appointment created successfully.")
            return redirect("appointment_list")
    else:
        form = DoctorAppointmentForm()

    return render(request, "patients/doctor_appointment.html", {"form": form})


@login_required
def appointment_list(request):
    """
    Displays a list of appointments for the logged-in patient.

    This view retrieves all appointments associated with the currently logged-in patient.
    If the user is not a registered patient, an empty list is shown.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered template displaying the list of appointments.
    """
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = DoctorAppointment.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        appointments = []  # If the user is not a patient, show an empty list

    return render(request, "patients/list.html", {"appointments": appointments})
# Patient Part End (Fatima)
