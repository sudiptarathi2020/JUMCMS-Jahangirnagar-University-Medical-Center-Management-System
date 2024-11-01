from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorAppointment
from django.contrib import messages
from users.models import Patient, Doctor
from datetime import date, timedelta

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
    return redirect("doctor-dashboard")


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
    age = calculate_detailed_age(patient.user.date_of_birth)
    context = {
        "doctor": doctor,
        "patient": patient,
        "age": age,
    }
    return render(request, "doctors/patient_information.htm", context)


def calculate_detailed_age(date_of_birth):
    """
    Calculates the detailed age of a person based on their date of birth.

    This function computes the age in years, months, and days given a date of birth.

    Parameters:
        date_of_birth (date): The date of birth of the person.

    Returns:
        str: A string representing the age in the format "X years, Y months, Z days".
    """
    today = date.today()

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
