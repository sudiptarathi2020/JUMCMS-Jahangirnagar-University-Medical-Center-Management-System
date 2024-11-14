from django.contrib import admin
from .models import Test, PrescribedTest, TestReport

admin.site.register(Test)
admin.site.register(PrescribedTest)
admin.site.register(TestReport)
