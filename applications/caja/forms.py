from .models import MovimientosCaja
from django import forms

class MovimientoNewForm(forms.ModelForm):
    class Meta:
        model=MovimientosCaja
        fields=['movimiento','monto','observacion','concepto']
        labels={'movimiento':'Movimiento','monto': 'Monto' , 'observacion':'Observacion' ,'concepto':'Concepto'}
        widget={'observacion':forms.TextInput}

def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
    super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
    for field in iter(self.fields):
        self.fields[field].widget.attrs.update({
            'class':'form-control',
        })
