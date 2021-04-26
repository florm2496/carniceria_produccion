from .models import Unidad,Producto
from django import forms


class UnidadNewForm(forms.ModelForm):
    class Meta:
        model=Unidad
        fields=['nombre','estado']
        labels={'nombre':'Nombre'}
        #widget={'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })

class ProductoNewForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['nombre','descripcion','codigo','tipo','precioventa','unidad','existencia','ultimacompra','estado','categoria','marca' ]
       
        widget={'descripcion':forms.TextInput, 'precioventa':forms.NumberInput(attrs={'required':True})}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
            self.fields['descripcion'].widget.attrs['required']=True
            self.fields['ultimacompra'].widget.attrs['readonly']=True
            self.fields['existencia'].widget.attrs['readonly']=True

    def clean(self):
        try:
            producto=Producto.objects.get(codigo=self.cleaned_data['codigo'])
            if not self.instance.pk:
                raise forms.ValidationError("El registro ya existe")
            elif self.instance.pk!=producto.pk:
                raise forms.ValidationError("Cambio no permitido")
        except Producto.DoesNotExist:
            pass
        return self.cleaned_data



