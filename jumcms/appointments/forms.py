from django import forms
from appointments.models import TestAppointment
from django.utils import timezone

class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = TestAppointment
        fields = ['appointment_date_time', 'status']
        widgets = {
            'appointment_date_time': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Select a future date and time'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_appointment_date_time(self):
        appointment_date_time = self.cleaned_data['appointment_date_time']
        if appointment_date_time <= timezone.now():
            raise forms.ValidationError("The appointment date and time must be in the future.")
        return appointment_date_time
