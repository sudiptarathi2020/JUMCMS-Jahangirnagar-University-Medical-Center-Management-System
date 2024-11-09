from django.urls import path
from medical_tests.controllers import *
app_name = 'medical_tests'
urlpatterns = [
    path('test-list/', prescribed_test_list, name='test-list'),
    path("create<int:prescribed_test_id>/",create_test_report, name="create-test-report"),
    path('report-list/', see_report_list, name="see-report-list"),
]
