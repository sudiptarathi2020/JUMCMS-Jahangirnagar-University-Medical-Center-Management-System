from django.contrib import admin

# Register your models here.

from certifications.models import FundraisingCertificate, FundraisingRequest
admin.site.register(FundraisingCertificate)
admin.site.register(FundraisingRequest)
