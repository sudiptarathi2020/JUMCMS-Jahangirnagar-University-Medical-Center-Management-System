from django.urls import path
from medicines.controllers import prescription_details, search_prescriptions

APP_NAME = 'medicines'
urlpatterns = [
    path('search/', search_prescriptions, name='search_prescriptions'),
    path('<int:prescription_id>/', prescription_details, name='prescription_details'),
]