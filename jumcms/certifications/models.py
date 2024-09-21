from django.db import models
from users.models import Patient


# Create your models here.
class FundraisingRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=255)
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField(null=True, blank=True)
    attachments = models.FileField(upload_to="fundraising/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for fundraising for {self.patient.name} suffering from {self.disease_name}"


class FundraisingCertificate(models.Model):
    fundraising_request = models.ForeignKey(
        FundraisingRequest, on_delete=models.CASCADE
    )
    certificate_issued_date = models.DateField(auto_now_add=True)
    attachments = models.FileField(
        upload_to="fundraising_certificates/", null=True, blank=True
    )

    def __str__(self):
        return f"Certificate for {self.fundraising_request.patient.name} on {self.certificate_issued_date}"
