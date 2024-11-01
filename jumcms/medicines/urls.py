from django.urls import path
from medicines.controllers import prescription_details, search_prescriptions, all_prescriptions

app_name = 'medicines'
urlpatterns = [
    path("", all_prescriptions, name="all_prescriptions"),
    path('search/', search_prescriptions, name='search_prescriptions'),

    path('prescription_details/<int:prescription_id>/', prescription_details, name='prescription_details'),
]