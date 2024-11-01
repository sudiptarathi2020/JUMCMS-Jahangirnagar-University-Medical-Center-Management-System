from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorAppointment
from django.contrib import messages

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
    appointment = get_object_or_404(DoctorAppointment, pk=pk)
    doctor = appointment.doctor
    appointment.delete()
    if doctor.no_of_appointments > 0:
        doctor.no_of_appointments -= 1
        doctor.save()
    messages.success(request, "Appointment deleted successfully.")
    return redirect("doctor-dashboard")


# Doctor part end
