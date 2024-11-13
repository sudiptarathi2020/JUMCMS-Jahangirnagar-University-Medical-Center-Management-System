from django.contrib import admin
from .models import User, Doctor, Patient, Storekeeper, LabTechnician
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'is_admin')
    search_fields = ('email', 'name')
    ordering = ('email',)

# Register the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Storekeeper)
admin.site.register(LabTechnician)
