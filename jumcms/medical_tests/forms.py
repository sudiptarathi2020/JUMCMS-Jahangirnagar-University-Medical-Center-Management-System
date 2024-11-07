from django import forms
from .models import TestReport

class TestReportForm(forms.ModelForm):
    class Meta:
        model = TestReport
        fields = ['prescribed_test', 'result', 'attached_file', 'notes']
