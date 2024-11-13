from django.contrib import admin

# Register your models here.

from medicines.models import Medicine, PrescribedMedicine, Prescription
admin.site.register(Medicine)
admin.site.register(PrescribedMedicine)
admin.site.register(Prescription)