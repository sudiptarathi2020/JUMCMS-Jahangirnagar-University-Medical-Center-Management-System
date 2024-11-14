from django.contrib import admin

# Register your models here.
from medical_tests.models import Test, PrescribedTest, TestReport

admin.site.register(Test)
admin.site.register(PrescribedTest)
admin.site.register(TestReport)
