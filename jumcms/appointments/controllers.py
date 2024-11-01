from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import LabTechnician
from django.contrib import messages
from appointments.models import TestAppointment
from appointments.forms import RescheduleAppointmentForm
# Create your views here.
from appointments.models import TestAppointment

@login_required
def test_appointments_list(request):
    """
    View function for displaying a list of test appointments for the logged-in lab technician.
    """
    if request.method == "POST":
        try:
            lab_technician = LabTechnician.objects.get(user=request.user)
            appointments = TestAppointment.objects.filter(lab_technician=lab_technician)
        except LabTechnician.DoesNotExist:
            messages.error(request, "You do not have permission to view test appointments.")
            return redirect('users:login') 
        return render(request, 'lab_technician/lab_technician_dashboard_list.htm', {'appointments': appointments,'lab_technician':lab_technician})
    else:
        return render(request,'lab_technician/lab_technician_dashboard.htm')


@login_required
def reschedule_test_appointment(request, appointment_id):
    # Retrieve the appointment by ID
    
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
        appointment = get_object_or_404(TestAppointment, id=appointment_id)
    
        if request.method == "POST":
            form = RescheduleAppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return render(request,"lab_technician/lab_technician_dashboard.htm/", {'lab_technician':lab_technician})
        else:
            form = RescheduleAppointmentForm(instance=appointment)
        
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect('appointments:test_appointments_fail')  # Adjust the redirect path as necessary
        

    return render(request, 'lab_technician/reschedule_test_appointment.html', {
        'form': form,
        'appointment': appointment,
        'lab_technician': lab_technician,
    })
