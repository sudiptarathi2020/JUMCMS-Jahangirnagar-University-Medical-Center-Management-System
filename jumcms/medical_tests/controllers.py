from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from medical_tests.models import TestReport
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
import logging
from medical_tests.models import PrescribedTest, Prescription
from medical_tests.forms import TestReportForm
from users.models import LabTechnician
# Create your views here.

@login_required
def prescribed_test_list(request):
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect('users:users-login')
    prescribed_tests = PrescribedTest.objects.all()
    
    return render(request,'lab_technician/list_of_prescribed_test.html',{'prescribed_tests':prescribed_tests,'lab_technician':lab_technician})


@login_required
def create_test_report(request, prescribed_test_id):
    """
    View to create a test report for a specific prescribed test.
    """
    prescribed_test = get_object_or_404(PrescribedTest, id=prescribed_test_id)

    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect('users:users-login')
    if request.method == "POST":
        form = TestReportForm(request.POST, request.FILES)
        if form.is_valid():
            test_report = form.save(commit=False)
            test_report.prescribed_test = prescribed_test
            test_report.save()
            messages.success(request, "Test report created successfully.")
            return redirect('medical_tests:list')  # Adjust this to match the correct list view name
        else:
            logging.error("Form is not valid: %s", form.errors)  # Logs errors if form is invalid
    else:
        form = TestReportForm()

    return render(request, 'lab_technician/create_test_report.html', {
        'form': form,
        'prescribed_test': prescribed_test,
        'lab_technician':lab_technician,
    })

@login_required
def see_report_list(request):
    try:
        lab_technician = LabTechnician.objects.get(user=request.user)
    except LabTechnician.DoesNotExist:
        messages.error(request, "You do not have permission to view test appointments.")
        return redirect('users:users-login')
    test_reports = TestReport.objects.all()
    
    return render(request,'lab_technician/list_of_report.html',{
        'lab_technician':lab_technician,
        'test_reports':test_reports,
    })
    