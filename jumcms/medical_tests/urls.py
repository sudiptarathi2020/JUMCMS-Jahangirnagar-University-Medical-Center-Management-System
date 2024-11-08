

from django.urls import path
from medical_tests.controllers import *

app_name = "medical_tests"
urlpatterns = [

     path("view_test_report/",view_test_report, name="view-test-report"),
     path("Download_test_report/<int:report_id>/",download_test_report,name="download-test-report"),
]
