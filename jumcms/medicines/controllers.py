from io import BytesIO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from medicines.forms import MedicineForm
from .models import Prescription, PrescribedMedicine


# StoreKeeper Part Start
@login_required
def all_prescriptions(request):
    """
    all prescriptions
    :param request:
    :return: list of all prescriptions
    """
    prescriptions = Prescription.objects.all()
    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'storekeeper/prescription_list.html', context)


@login_required
def search_prescriptions(request):
    """
    Allows lab technicians to search for prescriptions by patient name.
    :param request:
    :return: list of all prescriptions
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


@login_required
def prescription_details(request, prescription_id):
    """
    Displays details of a specific prescribed medicine.
    :param: prescription_id
    :return: html
    """
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescribed_medicines = (PrescribedMedicine.
                            objects.filter(prescription=prescription))

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
        if medicine.stock_quantity == 0:
            medicine.delete()


    context = {
        'prescription': prescription,
        'medicines_info': medicines_info,
    }
    return render(request, 'storekeeper/prescribed_medicine_details.html', context)


def generate_pdf(medicines_info,
                 doctor_name,
                 patient_name,
                 prescription_id):
    """
    Generates a PDF report of dispensed medicines.


    Args:
        medicines_info (list): A list of dictionaries containing medicine information.
        doctor_name (str): The name of the doctor who issued the prescription.
        patient_name (str): The name of the patient.
        prescription_id (int): The ID of the prescription.

    Returns:
        HttpResponse: An HTTP response containing the generated PDF file.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{prescription_id}.pdf"'
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    getSampleStyleSheet()

    elements = [Table([[f"Prescription ID: {prescription_id}"]]), Table([[f"Doctor: {doctor_name}"]],
                                                                        style=[('FONTSIZE', (0, 0), (-1, -1), 14), (
                                                                            'FONTNAME', (0, 0), (-1, -1),
                                                                            'Helvetica-Bold')]),
                Table([[f"Patient: {patient_name}"]],
                      style=[('FONTSIZE', (0, 0), (-1, -1), 14), ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')]),
                Table([["Dispensed Medicines:"]], style=[('FONTSIZE', (0, 0), (-1, -1), 14)])]

    # Add prescription details

    # Add dispensed medicines details

    # Create table data for medicines
    table_data = [["Medicine Name", "Required Quantity", "In Stock", "Frequency", "Instructions"]]
    for info in medicines_info:
        if info['is_stock_sufficient']:
            table_data.append([info['medicine_name'], info['required_quantity'], info['in_stock'], info['frequency'],
                               info['instructions']])

    # Create table with custom style
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def dispense_medicines(request, prescription_id):
    """
    Dispense medicines to patient
    :param: request, int
    :return: html
    """
    if request.method == 'POST':
        prescription = get_object_or_404(Prescription, id=prescription_id)
        prescribed_medicines = PrescribedMedicine.objects.filter(prescription=prescription)
        medicines_info = []
        for prescribed_medicine in prescribed_medicines:
            medicine = prescribed_medicine.medicine
            required_quantity = prescribed_medicine.duration  # Assuming the duration is the quantity needed
            in_stock = medicine.stock_quantity

            # Check if the stock is sufficient
            is_stock_sufficient = in_stock >= required_quantity

            if is_stock_sufficient:
                medicine.stock_quantity -= required_quantity
                medicine.save()
                medicines_info.append({
                    'medicine_name': medicine.name,
                    'required_quantity': required_quantity,
                    'in_stock': in_stock,
                    'is_stock_sufficient': is_stock_sufficient,
                    'frequency': prescribed_medicine.frequency,
                    'instructions': prescribed_medicine.instructions,
                })

        if medicines_info:
            messages.success(request, f"dispensed successfully.")
            pdf_response = generate_pdf(medicines_info, prescription.doctor_appointment.doctor.user.name,
                                        prescription.doctor_appointment.patient.user.name, prescription_id)
            return pdf_response

        else:
            messages.error(request, f"Not enough stock.")
            return redirect('medicines:search-prescriptions')
    else:
        return redirect('medicines:prescription-details', prescription_id)


@login_required
def add_medicine(request):
    user = request.user
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:storekeeper_dashboard')  # Replace with your actual success URL
    else:
        form = MedicineForm()
    return render(request, 'storekeeper/add_medicine.html', {'form': form, 'user': user})
