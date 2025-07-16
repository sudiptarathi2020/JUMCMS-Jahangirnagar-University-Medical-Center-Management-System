from django.contrib import admin
from .models import User, Doctor, Patient, Storekeeper, LabTechnician

# Register the models with the admin site
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Storekeeper)
admin.site.register(LabTechnician)
