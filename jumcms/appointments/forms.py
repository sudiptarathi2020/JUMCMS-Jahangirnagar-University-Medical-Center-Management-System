from django import forms
from appointments.models import DoctorAppointment
from users.models import Doctor


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
