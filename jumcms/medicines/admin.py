from django.contrib import admin

# Register your models here.
from medicines.models import Medicine, Prescription, PrescribedMedicine

admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(PrescribedMedicine)
