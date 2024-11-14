from django import forms
from appointments.models import TestAppointment, DoctorAppointment
from django.utils import timezone
from users.models import Doctor


class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = TestAppointment
        fields = ["appointment_date_time", "status"]
        widgets = {
            "appointment_date_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a future date and time",
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_appointment_date_time(self):
        appointment_date_time = self.cleaned_data["appointment_date_time"]
        if appointment_date_time <= timezone.now():
            raise forms.ValidationError(
                "The appointment date and time must be in the future."
            )
        return appointment_date_time


class DoctorAppointmentCreationForm(forms.ModelForm):
    appointment_date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )
    )
    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Reason for appointment",
                "class": "form-control",
            }
        )
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    is_emergency = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = DoctorAppointment
        fields = ["doctor", "appointment_date_time", "reason", "is_emergency"]
