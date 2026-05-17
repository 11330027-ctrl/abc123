from django.db import models
from django import forms
from django.utils import timezone
from .models import RentalRecord, Device

class RentalForm(forms.ModelForm):
    
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'id_date'}), initial=timezone.now, label="日期")
    period = forms.ChoiceField(choices=RentalRecord.PERIODS, initial=1, widget=forms.Select(attrs={'id': 'id_period'}), label="節次")
    school_section = forms.ChoiceField(choices=Device.SCHOOL_SECTIONS, widget=forms.Select(attrs={'id': 'id_school_section'}), label="學部")
    device = forms.ModelChoiceField(queryset=Device.objects.none(), widget=forms.Select(attrs={'id': 'id_device'}), label="載具")

    class Meta:
        model = RentalRecord
        fields = ['date', 'period', 'school_section', 'student_name', 'student_class', 'device', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get('device')
        quantity = cleaned_data.get('quantity')

        if device:
            if device.is_bulk:
                if device.device_type in ['ipad', 'surface_go', 'acer_laptop'] and quantity >= 20:
                    raise forms.ValidationError("散裝 iPad/SurfaceGo/Acer筆電 的借用數量必須少於 20 台！")
                if device.device_type == 'chromebook' and quantity >= 15:
                    raise forms.ValidationError("散裝 Chromebook 的借用數量必須少於 15 台！")
            else:
                cleaned_data['quantity'] = 1
        return cleaned_data



# Create your tests here.
