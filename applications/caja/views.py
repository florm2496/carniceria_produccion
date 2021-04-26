from django.shortcuts import render
from .models import *
from django.db import models
from django.views.generic import CreateView , ListView
from django.urls import reverse_lazy
from .forms import MovimientoNewForm
from applications.ventas.models import FacturaEnc,FacturaDet
from applications.ventas.managers import FacturaDetManager,FacturaEncManager
# Create your views here.
from django.http import HttpResponse


class MovimientosCajaCreateView(CreateView):
    model=MovimientosCaja
    template_name='caja/operaciones.html'
    form_class=MovimientoNewForm
    success_url=reverse_lazy('caja:listaoperaciones')
        
    
    
    

class ListaOperacionesListView(ListView):
    model=MovimientosCaja
    template_name='caja/listaoperaciones.html'
    context_object_name='obj'
    
    def get_context_data(self, **kwargs):
        caja=Caja.objects.first()
        monto_actual=caja.monto_actual

        movimientos=MovimientosCaja.objects.all()
        conceptos=Concepto.objects.all()
        print(conceptos)
        print(monto_actual)
        context = {'montoactual':monto_actual,
                   'movimientos':movimientos,
                   'conceptos':conceptos,
                    }
        return context

    #monto inicial a la hora de apertura
    #cuanto en egresos
    #cuanto en ingresos
    #cuanto en ventas
    #cuanto en compras (???)
    #total que queda

    #que usuario hace cada movimiento , a que hora y que fecha

    #el boton de cierre de caja deberia activar esta vista de funcion , recolectar y hacer los calculos necesarios
    # y luego mostrarlos. Cada cierre de caja se guarda , entonces es un modelo

def DetalleCaja(request):
    template_name='caja/caja.html'
    caja=Caja.objects.last()
    monto_actual=caja.monto_actual
    monto_inicial=caja.monto_inicial
    contexto={'monto_actual':monto_actual ,'monto_inicial':monto_inicial}
    return render(request,template_name,contexto)



