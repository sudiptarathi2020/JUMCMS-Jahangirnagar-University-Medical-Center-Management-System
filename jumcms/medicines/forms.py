# forms.py
from django import forms
from medicines.models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name',
            'generic_name',
            'manufacturer',
            'dosage_form',
            'strength',
            'description',
            'price',
            'stock_quantity',
            'expiry_date',
            # 'prescription_required',  # Uncomment if you decide to use this field
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
