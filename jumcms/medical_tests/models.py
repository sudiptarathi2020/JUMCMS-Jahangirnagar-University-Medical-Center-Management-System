from django.db import models
from medicines.models import Prescription


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PrescribedTest(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="prescribed_tests"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.test.name} for {self.prescription.doctor_appointment.patient}"


class TestReport(models.Model):
    prescribed_test = models.ForeignKey(
        PrescribedTest, on_delete=models.CASCADE, related_name="test_reports"
    )
    report_date = models.DateField(auto_now_add=True)
    result = models.TextField()
    attached_file = models.FileField(upload_to="test_reports/", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Report for {self.prescribed_test.test.name} on {self.report_date}"