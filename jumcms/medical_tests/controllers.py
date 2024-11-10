# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TestReport
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from users.models import Patient, User
from io import BytesIO


@login_required
def view_test_report(request):
    """
    Display a list of test reports for the authenticated patient.

    This view retrieves all test reports associated with the logged-in user
    (assuming the user is a patient) by querying based on their patient profile.
    The reports are then rendered as HTML for viewing.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - HttpResponse: Renders 'patients/view_test_report.html' template with the
      list of test reports for the patient.
    """
    patient = Patient.objects.get(user=request.user)
    reports = TestReport.objects.filter(prescribed_test__prescription__doctor_appointment__patient_id=patient.id)
    return render(request, "patients/view_test_report.html", {"reports": reports,"patient":patient})

@login_required
def download_test_report(request, report_id):
    """
    Generate and download a specific test report as a PDF.

    This view allows an authenticated patient to download a PDF version of a
    specific test report, identified by `report_id`. The report is rendered
    to a PDF format using the xhtml2pdf library.

    Parameters:
    - request: HttpRequest object containing metadata about the request.
    - report_id (int): ID of the TestReport to be downloaded.

    Returns:
    - HttpResponse: PDF response with 'application/pdf' content type if the PDF
      is successfully generated.
    - HttpResponse: Returns a 400 error response if PDF generation fails.
    """
    report = get_object_or_404(TestReport, id=report_id)
    template_path = "patients/pdf_report_template.html"

    # Render HTML to a string
    html = render_to_string(template_path, {"report": report})

    # Generate the PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="TestReport_{report_id}.pdf"'

    # Use xhtml2pdf to convert HTML to PDF
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)

    if pisa_status.err:
        return HttpResponse("Error creating PDF", status=400)
    else:
        return response
