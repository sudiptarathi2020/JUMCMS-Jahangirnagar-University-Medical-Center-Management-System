from django import forms
from appointments.models import TestAppointment
from django.utils import timezone

class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = TestAppointment
        fields = ['appointment_date_time', 'status']

    def clean_appointment_date_time(self):
        appointment_date_time = self.cleaned_data['appointment_date_time']
        if appointment_date_time <= timezone.now():
            raise forms.ValidationError("The appointment date and time must be in the future.")
        return appointment_date_time