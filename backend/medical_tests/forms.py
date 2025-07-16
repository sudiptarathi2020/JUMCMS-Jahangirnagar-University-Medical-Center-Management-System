from django import forms
from .models import TestReport

class TestReportForm(forms.ModelForm):
    """
    Form for creating and updating a TestReport.

    This form handles the fields required for a lab technician to submit
    a test report, including the result, an attached file, and optional notes.

    :param result: Text area for lab result details.
    :type result: TextField
    :param attached_file: Field for attaching files related to the test report.
    :type attached_file: FileField
    :param notes: Optional text area for additional notes.
    :type notes: TextField
    """

    class Meta:
        model = TestReport
        fields = ['result', 'attached_file', 'notes']
        widgets = {
            'result': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """
        Custom clean method for additional validation on form data.

        This method can be extended to add custom validation logic if necessary.
        
        :return: Cleaned data with any additional validation applied.
        :rtype: dict
        """
        cleaned_data = super().clean()
        # Add any custom validation here if needed
        return cleaned_data
