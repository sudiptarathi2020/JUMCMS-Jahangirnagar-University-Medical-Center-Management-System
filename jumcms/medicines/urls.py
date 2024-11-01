from django.urls import path
from medicines.controllers import prescription_details, search_prescriptions, all_prescriptions, dispense_medicines

app_name = 'medicines'
urlpatterns = [
    path("", all_prescriptions, name="all_prescriptions"),
    path('search/', search_prescriptions, name='search-prescriptions'),

    path('prescription-details/<int:prescription_id>/', prescription_details, name='prescription-details'),
    path('dispense/<int:prescription_id>/', dispense_medicines, name="dispense-medicines"),
]
