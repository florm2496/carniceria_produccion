from django import forms

from .models import Animal,Res



class AnimalNewForm(forms.ModelForm):
    class Meta:
        model=Animal
        fields=(
            'tropa',
            'peso_animal'
        )

class ResEditForm(forms.ModelForm):
    class Meta:
        model=Res
        fields=('animal','nombre','peso','vendida')
        #METODO 1
         
    #METODO 2
    def __init__(self, *args, **kwargs):
        super(ResEditForm, self).__init__(*args, **kwargs)
        self.fields['animal'].widget.attrs['readonly']=True
        self.fields['nombre'].widget.attrs['readonly']=True
        self.fields['vendida'].widget.attrs['readonly']=True
        #self.fields['nombre'].widget.attrs['disabled']='disabled'

