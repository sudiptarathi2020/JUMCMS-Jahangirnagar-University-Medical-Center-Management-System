from django.urls import path
from medical_tests.controllers import submit_test_report 
app_name = 'medical_tests'
urlpatterns = [
    path('submit-test-report/', submit_test_report, name='submit_test_report'),
]
