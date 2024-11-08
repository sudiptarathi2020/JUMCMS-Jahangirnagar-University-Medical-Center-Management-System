from django.urls import path
from medical_tests.controllers import *
app_name = 'medical_tests'
urlpatterns = [
    path('list/', prescribed_test_list, name='list'),
    path("create<int:prescribed_test_id>/",create_test_report, name="create-test-report"),
]
