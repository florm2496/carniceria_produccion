from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre',
            'numero','direccion','estado']
        exclude = ['um','fm','fc']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['numero'].widget.attrs['requiered']=False
            self.fields['direccion'].widget.attrs['requiered']=False