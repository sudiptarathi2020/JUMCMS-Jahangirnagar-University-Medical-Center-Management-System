from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import LabTechnician
from appointments.models import TestAppointment
from appointments.forms import RescheduleAppointmentForm


@login_required
def test_appointments_list(request):
    """
    Displays a list of test appointments for the logged-in lab technician.

    Retrieves the test appointments associated with the logged lab technician when
    the request is a POST. If the lab technician does not exist, an error message is 
    displayed, and the user is redirected to the login page.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from the logged-in user.

    Returns
    -------
    HttpResponse
        If appointments are retrieved, renders the 'lab_technician_dashboard_list.htm' 
        template with the appointments and lab technician context.
        If the request method is not POST, renders 'lab_technician_dashboard.htm'.
    """
    if request.method == "POST":

        try:
            lab_technician = LabTechnician.objects.get(user=request.user)
        except LabTechnician.DoesNotExist:
            messages.error(request, "You do not have permission to view test appointments.")
            return redirect('users:users-login')

        appointments = TestAppointment.objects.filter(lab_technician=lab_technician)

        return render(
            request,
            'lab_technician/lab_technician_dashboard_list.htm',
            {'appointments': appointments, 'lab_technician': lab_technician}
        )

    return render(request, 'lab_technician/lab_technician_dashboard.htm')


@login_required
def reschedule_test_appointment(request, appointment_id):
    """
    Reschedules a specific test appointment for the lab technician.

    Attempts to retrieve the appointment by its ID. If the lab technician does not exist, 
    an error message is displayed, and the user is redirected to a failure page. If the 
    request is a POST and the form is valid, the rescheduled appointment is saved.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object from the logged-in user.
    appointment_id : int
        The ID of the appointment to be rescheduled.

    Returns
    -------
    HttpResponse
        If the form is successfully saved, renders 'lab_technician_dashboard.htm'.
        Otherwise, renders 'reschedule_test_appointment.html' with the form, appointment,
        and lab technician context.
    """
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
        appointment = get_object_or_404(TestAppointment, id=appointment_id)

        if request.method == "POST":
            form = RescheduleAppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return render(
                    request,
                    "lab_technician/lab_technician_dashboard.htm",
                    {'lab_technician': lab_technician}
                )
        else:
            form = RescheduleAppointmentForm(instance=appointment)

    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect('appointments:test_appointments_fail')

    return render(request, 'lab_technician/reschedule_test_appointment.html', {
        'form': form,
        'appointment': appointment,
        'lab_technician': lab_technician,
    })
