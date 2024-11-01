from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Prescription, PrescribedMedicine


@login_required
def all_prescriptions(request):
    prescribed_medicines = PrescribedMedicine.objects.all()
    context = {
        'prescribed_medicines': prescribed_medicines,
    }
    return render(request, 'storekeeper/prescription_list.html', context)

@login_required
def search_prescriptions(request):
    """
    Allows lab technicians to search for prescriptions by patient name.
    """
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        prescriptions = Prescription.objects.filter(
            Q(doctor_appointment__patient__user__name__icontains=patient_name)
        )
        context = {
            'prescriptions': prescriptions,
            'user': request.user,
        }
        return render(request, 'storekeeper/prescription_list.html', context)
    else:
        return render(request, 'storekeeper/prescription_search.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import PrescribedMedicine, Prescription


@login_required
def prescription_details(request, prescription_id):
    """
    Displays details of a specific prescribed medicine.
    """
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescribed_medicines = PrescribedMedicine.objects.filter(prescription=prescription)

    # Prepare the context with stock information
    medicines_info = []
    for prescribed_medicine in prescribed_medicines:
        medicine = prescribed_medicine.medicine
        required_quantity = prescribed_medicine.duration  # Assuming the duration is the quantity needed
        in_stock = medicine.stock_quantity

        # Check if the stock is sufficient
        is_stock_sufficient = in_stock >= required_quantity
        medicines_info.append({
            'medicine_name': medicine.name,
            'required_quantity': required_quantity,
            'in_stock': in_stock,
            'is_stock_sufficient': is_stock_sufficient,
            'frequency': prescribed_medicine.frequency,
            'instructions': prescribed_medicine.instructions,
        })

    context = {
        'prescription': prescription,
        'medicines_info': medicines_info,
    }
    return render(request, 'storekeeper/prescribed_medicine_details.html', context)
