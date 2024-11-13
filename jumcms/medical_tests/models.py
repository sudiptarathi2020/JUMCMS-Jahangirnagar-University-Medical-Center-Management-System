from django.db import models
from medicines.models import Prescription


class Test(models.Model):
    """
    Model representing a medical test.

    Attributes:
        name (CharField): Name of the test.
        description (TextField): Optional description of the test.
        department (CharField): Department associated with the test.
        is_available (BooleanField): Indicates if the test is currently available.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns a string representation of the Test object.

        :return: Test name.
        :rtype: str
        """
        return self.name


class PrescribedTest(models.Model):
    """
    Model representing a prescribed test linked to a prescription.

    Attributes:
        prescription (ForeignKey): Reference to the associated prescription.
        test (ForeignKey): Reference to the test that has been prescribed.
    """

    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="prescribed_tests"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the PrescribedTest object.

        :return: Test name and associated patient.
        :rtype: str
        """
        return f"{self.test.name} for {self.prescription.doctor_appointment.patient}"


class TestReport(models.Model):
    """
    Model representing a test report for a prescribed test.

    Attributes:
        prescribed_test (ForeignKey): Reference to the associated prescribed test.
        report_date (DateField): Date when the report was created.
        result (TextField): The result of the test.
        attached_file (FileField): Optional file attachment for the report.
        notes (TextField): Optional notes about the test or its results.
    """

    prescribed_test = models.ForeignKey(
        PrescribedTest, on_delete=models.CASCADE, related_name="test_reports"
    )
    report_date = models.DateField(auto_now_add=True)
    result = models.TextField()
    attached_file = models.FileField(upload_to="test_reports/", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the TestReport object.

        :return: Report description including test name and report date.
        :rtype: str
        """
        return f"Report for {self.prescribed_test.test.name} on {self.report_date}"