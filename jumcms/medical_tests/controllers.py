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
    """View the test report as HTML."""
    patient = Patient.objects.get(user=request.user)
    reports = TestReport.objects.filter(prescribed_test__prescription__doctor_appointment__patient_id=patient.id)
    return render(request, "patients/view_test_report.html", {"reports": reports,"patient":patient})

@login_required
def download_test_report(request, report_id):
    """Download the test report as a PDF."""
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
    
    return response
