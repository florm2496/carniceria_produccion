from django import forms
from django.core.exceptions import ValidationError
from .models import ComprasEnc


class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()

    
    class Meta:
        model=ComprasEnc
        fields=['fecha_compra','observacion',
            'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
    
    def clean_fecha_compra(self):
        fecha_compra= self.cleaned_data.get('fecha_compra')
        print(fecha_compra)
        if fecha_compra=='':

            raise ValidationError('El campo fecha esta vacio')