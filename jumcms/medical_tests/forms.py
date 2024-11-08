from django import forms
from .models import TestReport

class TestReportForm(forms.ModelForm):
    class Meta:
        model = TestReport
        fields = ['result', 'attached_file', 'notes']
        widgets = {
            'result': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here if needed
        return cleaned_data
