"""
Admin module for managing models in the Django admin interface.

This module registers the models `Medicine`, `Prescription`, and
`PrescribedMedicine` with the Django admin site, allowing them to
be managed through the admin interface.

Classes:
    None

Functions:
    None

Modules:
    admin: Django admin module used to manage the admin interface.

Attributes:
    admin.site.register: Registers the provided models with the Django admin site.
"""

from django.contrib import admin
from .models import Medicine, Prescription, PrescribedMedicine

# Registering the Medicine model
admin.site.register(Medicine)
"""
Registers the `Medicine` model with the Django admin site.

This allows the admin user to add, view, edit, and delete `Medicine` records
through the Django admin interface.
"""

# Registering the Prescription model
admin.site.register(Prescription)
"""
Registers the `Prescription` model with the Django admin site.

This enables the admin interface for managing prescriptions, including
the ability to add, view, edit, and delete prescription records.
"""

# Registering the PrescribedMedicine model
admin.site.register(PrescribedMedicine)
"""
Registers the `PrescribedMedicine` model with the Django admin site.

Admin users can manage the relationship between prescriptions and
the medicines prescribed through the admin interface.
"""
