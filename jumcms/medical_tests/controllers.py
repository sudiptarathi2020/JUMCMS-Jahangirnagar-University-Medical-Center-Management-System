from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from medical_tests.models import TestReport
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from medical_tests.models import PrescribedTest, Prescription
from .forms import TestReportForm
# Create your views here.

@login_required
def submit_test_report(request):
    if request.method == "POST":
        form = TestReportForm(request.POST, request.FILES)
        if form.is_valid():
            test_report = form.save(commit=False)
            test_report.report_date = timezone.now()
            test_report.save()
            messages.success(request, "Test report submitted successfully.")
            return redirect(reverse('submit_test_report'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TestReportForm()

    prescribed_tests = PrescribedTest.objects.all()
    context = {
        'form': form,
        'prescribed_tests': prescribed_tests,
        'today_date': timezone.now().date(),
    }
    return render(request, 'lab_technician/submit_test_report.htm', context)
