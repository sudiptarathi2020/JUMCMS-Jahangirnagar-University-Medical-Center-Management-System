# appointments/forms.py

from django import forms
from appointments.models import DoctorAppointment
from users.models import Doctor

class DoctorAppointmentForm(forms.ModelForm):
    """
    A form for creating doctor appointments.

    This form allows users to schedule appointments with doctors by selecting a doctor,
    providing the appointment date and time, and specifying the reason for the appointment.

    Attributes:
        appointment_date_time (DateTimeField): The date and time for the appointment, 
                                                 rendered as a datetime-local input.
        reason (CharField): The reason for the appointment, rendered as a textarea input.
        doctor (ModelChoiceField): A dropdown selection of available doctors.

    Meta:
        model (DoctorAppointment): The model associated with this form.
        fields (list): A list of fields to include in the form, specifically 'doctor', 
                       'appointment_date_time', and 'reason'.
    """
    # Customize fields with widgets for improved user experience
    appointment_date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Reason for appointment', 'class': 'form-control'})
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = DoctorAppointment
        fields = ['doctor', 'appointment_date_time', 'reason']
