from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from medical_tests.models import TestReport
from django.contrib import messages
import logging
from medical_tests.models import PrescribedTest
from medical_tests.forms import TestReportForm
from users.models import LabTechnician
from django.http import HttpResponse
from .models import TestReport
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from users.models import Patient
from io import BytesIO


@login_required
def prescribed_test_list(request):
    """
    View function to display the list of prescribed tests for a logged-in lab technician.

    Retrieves a list of prescribed tests available for the lab technician.
    If the user is not a lab technician, redirects them to the login page with an error message.

    :param request: HTTP request object.
    :type request: HttpRequest
    :return: Rendered template displaying the list of prescribed tests.
    :rtype: HttpResponse
    """
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect("users:users-login")
    prescribed_tests = PrescribedTest.objects.all()

    return render(
        request,
        "lab_technician/list_of_prescribed_test.html",
        {
            "prescribed_tests": prescribed_tests,
            "lab_technician": lab_technician,
        },
    )


@login_required
def create_test_report(request, prescribed_test_id):
    """
    View function to create a test report for a specific prescribed test.

    Retrieves the prescribed test based on the ID. If a valid POST request is made,
    the test report is saved and associated with the prescribed test.
    If the form is invalid, errors are logged, and the form is re-rendered.

    :param request: HTTP request object.
    :type request: HttpRequest
    :param prescribed_test_id: ID of the prescribed test to create a report for.
    :type prescribed_test_id: int
    :return: Rendered template for creating a test report or redirect to the test list.
    :rtype: HttpResponse
    """
    prescribed_test = get_object_or_404(PrescribedTest, id=prescribed_test_id)

    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect("users:users-login")
    if request.method == "POST":
        form = TestReportForm(request.POST, request.FILES)
        if form.is_valid():
            test_report = form.save(commit=False)
            test_report.prescribed_test = prescribed_test
            test_report.save()
            messages.success(request, "Test report created successfully.")
            return redirect(
                "medical_tests:see-report-list"
            )  # Adjust this to match the correct list view name
        else:
            logging.error("Form is not valid: %s", form.errors)
    else:
        form = TestReportForm()

    return render(
        request,
        "lab_technician/create_test_report.html",
        {
            "form": form,
            "prescribed_test": prescribed_test,
            "lab_technician": lab_technician,
        },
    )


@login_required
def see_report_list(request):
    """
    View function to display a list of all test reports for the lab technician.

    Retrieves all test reports and renders them on a list page. If the user is not a lab technician,
    they are redirected with an error message.

    :param request: HTTP request object.
    :type request: HttpRequest
    :return: Rendered template showing a list of test reports.
    :rtype: HttpResponse
    """
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect("users:users-login")
    test_reports = TestReport.objects.all()

    return render(
        request,
        "lab_technician/list_of_report.html",
        {
            "lab_technician": lab_technician,
            "test_reports": test_reports,
        },
    )


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
    reports = TestReport.objects.filter(
        prescribed_test__prescription__doctor_appointment__patient_id=patient.id
    )
    return render(
        request,
        "patients/view_test_report.html",
        {"reports": reports, "patient": patient},
    )


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
    response["Content-Disposition"] = (
        f'attachment; filename="TestReport_{report_id}.pdf"'
    )

    # Use xhtml2pdf to convert HTML to PDF
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)

    if pisa_status.err:
        return HttpResponse("Error creating PDF", status=400)
    else:
        return response
