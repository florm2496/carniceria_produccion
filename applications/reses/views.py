from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from datetime import datetime
# Create your views here.
from .models import Tropa,Animal,Res,EncVentaReses,DetalleVentaRes,PagoReses,MedioPago,PagoCliente
from applications.ventas.models import Cliente
from django.views.generic import CreateView , UpdateView,ListView,FormView

from .forms import AnimalNewForm,ResEditForm
from django.db.models import Sum

from django.http import JsonResponse
import json
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin


class TropaNew(CreateView):
    model=Tropa
    fields='__all__'
    template_name='reses/añadirtropa.html'
    object_name='obj'
    success_url=reverse_lazy('reses:lista_tropas')


class TropaUpdate(UpdateView):
    model=Tropa
    fields='__all__'
    template_name='reses/añadirtropa.html'
    object_name='obj'
    success_url=reverse_lazy('reses:lista_tropas')

class TropasList(ListView):
    model=Tropa
    context_object_name='obj'
    template_name='reses/lista_tropas.html'


def AnimalNew(request,**kwargs):
    template_name='reses/nuevo_animal.html'
    contexto={}
    
    animal={}
    #OBTENGO EL ID PASADO EN LA URL PARA PODER FILTRAR LA TOPA CORRESPONDIENTE
    ID= kwargs['pk']
    tropa=Tropa.objects.filter(id=ID)
    

    if request.method=='POST':
            #OBTENGO EL ID DEL FORMULARIO
            id_tropa=request.POST.get('tropa')
            #CON ESE ID OBTENGO EL OBJETO,PORQUE SE DEBE GUARDAR UNA INSTANCIA DEL OBJETO , NO SU ID
            tropa=Tropa.objects.get(pk=id_tropa) #USO GET PORQUE OBTENGO DIRECTAMENTE EL OBJETO , SI USO FILTER OBTENGO UN QUERYSET
            peso_animal=request.POST.get('peso_animal')
           
            #obtener el numnero del animal anterior
            anm_ant=Animal.objects.filter(tropa=id_tropa).last()
            print(anm_ant)
            if anm_ant is None:
                num=0
            else:
                num=anm_ant.numero
                

            animal=Animal(
                numero=num+1,
                tropa=tropa,
                peso_animal=peso_animal,

            )  
            animal.save()
            #animal.ident='animal:{}-{}'.format(animal.id , animal.tropa)
            #animal.save()
            #HASTA AQUI ESTA CUBIERTA LA CREACION DEL ANIMAL

            
            return redirect('reses:animales',pk=ID) #se pasa el id  para filtrar el listado de animales segun la tropa


           

    contexto={
        'tropa':tropa,
    }

    return render(request, template_name,contexto)
 
class AnimalesList(ListView):
    model=Animal 
    template_name='reses/lista_animales.html'
    
    
    def get_context_data(self, **kwargs):
        context=super(AnimalesList , self).get_context_data(**kwargs)
        id=self.kwargs['pk']

        context['lista']=Animal.objects.filter(
            tropa=id
        )
        return context


class ResesList(ListView):
    model=Res
    context_object_name='obj'
    template_name = "reses/lista_reses.html"

class ResUpdate(UpdateView):
    model=Res
    form_class=ResEditForm
    #fields=('animal','nombre','peso','vendida')
    template_name = "reses/nueva_res.html"
    context_object_name='obj'
    success_url=reverse_lazy('reses:lista_reses')
    


    
######################################################################################

def VentaReses(request , id=None):
    template_name='reses/formventareses.html'
    encabezado={
        'fecha':datetime.today(),
    }
    detalle={}
    clientes=Cliente.objects.filter(estado=True).order_by('id')
    
    reses=Res.objects.filter(vendida=False)
    medios_pago=MedioPago.objects.all()
    
    if request.method=='GET':
        """cuando se quiere ver una venta ya creada , entonces el id
        en la url lo pasa a la vista y filtra ese encabezado """
        enc=EncVentaReses.objects.filter(pk=id).first()
        if not enc:
            #si no lo encuentra quiere decir que se quiere crear una nueva venta
            #entonces se inicializa el formulario del encabezado
            encabezado={
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'observacion':'',
                'total': 0.00,
                
            }
            #como la venta es nueva aun no tiene ningun detalle creado
            detalle=None
        #de lo contrario si el encabezado de la venta ya existe se inicializan los valores
        else:
            encabezado={
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                #'sub_total':enc.sub_total,
                #'descuento':enc.descuento,
                'observacion':enc.observacion,
                'total':enc.total
               
            }
        #esta sentencia no deberia ir dentro del else(???)
        detalle=DetalleVentaRes.objects.filter(venta=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes,'reses':reses ,'medios_pago':medios_pago}
        return render(request,template_name,contexto)
    
    if request.method=='POST':
        #Se recupera el cliente id seleccionado
        cliente=request.POST.get("enc_cliente")
        #con el id se obtiene la instancia del cliente
        cli=Cliente.objects.get(pk=cliente)

        #luego se obtiene la fecha 
        fecha=request.POST.get("enc_fecha")

        total=request.POST.get("total")
        
        observacion=request.POST.get('observacion') 
        print('observacion',observacion)  

        
        #si no existe un detalle de venta(?)
        if not id:
            enc=EncVentaReses(
                cliente=cli,
                fecha=fecha,
                total=0.00,
                observacion=observacion,

            )
            #si se crea el encabezado
            if enc:
                #se lo guarda
                enc.save()
                id=enc.id
        else:
            #si existe se filtra el encabezado por ese id
            enc=EncVentaReses.objects.filter(pk=id).first()
            if enc:
                enc.cliente=cli
                enc.save()
            if not id:
                messages.error(request , "No se puede continuar ,Numero de factura no detectado")
            #return redirect("ventas:ventas")

        id_res=request.POST.get('id_res')
        print(id_res)
        res=Res.objects.get(pk=id_res)

        precio=request.POST.get("id_precio_detalle")
        subtotal=request.POST.get('id_sub_total_detalle')

        det=DetalleVentaRes(
            venta=enc,
            res=res,
            precio=precio,
            subtotal=subtotal,
        )
        if det:
            det.save()
            venta=DetalleVentaRes.objects.filter(venta=enc.id)
            
            subtotal=venta.aggregate(Sum('subtotal'))
            enc.total = subtotal["subtotal__sum"]
            enc.save()

        return redirect('reses:editarventares',id=id)


    return render(request,template_name,contexto)
    
    

#esta vista procesa el json enviado desde el frontend y crea los pagos relacionado a la venta en cuestion
def PagoVentaAjax(request):
    template_name='reses/modal_pago_ajax.html'
    context={}

    print('recibiendo el json')

    if request.is_ajax():
        json_data = json.loads(request.body)
        
        #obtener id de la venta que viene en el json    
        id_venta=json_data['datos_venta'][0]['id']
        print(id_venta)
        #obtener instancia de venta
        venta=EncVentaReses.objects.get(pk=int(id_venta))
        print(venta)
        for item in json_data['pagos']:
            pago=PagoReses(
                monto=item['monto'], 
                medio=MedioPago.objects.get(pk=item['medio']),
                venta=venta,

                )
            pago.save()


        

    elif request.method is 'POST' or request.method is 'post':

        print('post')
    else:
        print('ocurrio un error')

    return render(request, template_name,context)


class ListaVentasReses(ListView):
    model=EncVentaReses 
    template_name='reses/listaresesvendidas.html'
    context_object_name='obj'


class CrearPagoCliente(CreateView):
    model=PagoCliente
    template_name="reses/modal_pago_cliente.html"
    fields='__all__'
    success_url=reverse_lazy('ventas:lista_clientes')
    success_message='Pago realizado con exito'

    
    def get_context_data(self, **kwargs):
        id_cliente = self.kwargs['id']
        cliente=Cliente.objects.get(pk=id_cliente)
        medios_pago=MedioPago.objects.filter(estado=True)
        context={
            'cliente':cliente,
            'cliente_id':cliente.id,
            'saldo':cliente.saldo , 
            'medios_pago':medios_pago
            }
        return context


class ListaPagosCliente(ListView):
    model=PagoCliente
    template_name='reses/lista_pagos_cliente.html'

    def get_context_data(self, **kwargs):
        id_cliente = self.kwargs['id']
        cliente=Cliente.objects.get(pk=id_cliente)
        pagos=PagoCliente.objects.filter(cliente=id_cliente)
        context={'obj':pagos,'cliente':cliente}
        return context
    
 
'''       
        
def PagoCliente(request,id):
    template_name="reses/modal_pago_cliente.html"
    cliente=Cliente.objects.get(pk=id)
    
    medios_pago=MedioPago.objects.all(estado=True)
    context={'medios_pago':medios_pago}

    if request.method=='POST':
        medio_pago=request.POST.get("medios_pago")
        monto=request.POST.get('monto')
        pago_cliente=PagoCliente( 
            medio_pago=MedioPago.objects.get(pk=medio_pago),
            monto=monto
            )
        pago_cliente.save()
    return render(request, template_name,context)




 
        



#class VentaResesEdit()
 def get_queryset(self):
        obj = super(VentaResesList, self).get_queryset()
        
        return obj.filter(vendida=True)
class AñadirAnimal(CreateView):
    model=Animal
    template_name='reses/animal.html'
    fields=('tropa','peso_animal')
    #form_class=AnimalForm
    #context_object_name='obj'
    success_url=reverse_lazy('reses:listareses')

    #esto funciona , pero no guardaba el ID hasta hacerse efectivo el ID en la base de datos. ya se el id definido en los modelos
    #o el que proporciona la ORM.
    #Si funcionaba con los otros campos
    #no se asigna id a un registro hasta que este se guarda con exito en la base de datos


    def form_valid(self,form):
        animal=form.save(commit=False)
        animal.ident='animal:{}-tropa{}'.format(animal.ID, animal.tropa)
        animal.save()

        return super(AñadirAnimal ,self).form_valid(form)

soluciones para crear las reses automaticamente luego de crear el animal:
1-
 
def CrearRes():
    animal=Animal.objects.last()
    res=Res(
        animal=animal,
        peso_inicial=0,
        peso_final=0,
        uc=animal.uc,
        
    )
    res.save()

llamando a la funcion al final de  la vista de añadir animal 
resultado: funcionaba pero la funcion se ejecutaba antes de crear el animal nuevo 
, por lo tanto agarraba el anterior y no el actual

class AñadirAnimal(FormView):
    #en el form view no hace falta asignar un modelo , este ya se asigna en el form relacionado a la vista
    template_name='reses/animal.html'
    form_class=AnimalForm
    context_object_name='obj'
    success_url=reverse_lazy('reses:tropas')
    

    def get_context_data(self, **kwargs):
        #este id lo obtengo de la URL
        ID= self.kwargs['pk']
        print('id',ID)

        context=super(AñadirAnimal , self).get_context_data(**kwargs)
        #HAGO FILTRO POR ID PARA ENVIAR SOLO LA TROPA CORRESPONDIENTE
        context['tropa']=Tropa.objects.filter(id=ID)
        print('----',context['tropa'])
        return context
    

    def form_valid(self,form):
        #de esta forma no se interactua directamente con la ORM de django
        
        animal=Animal(
            tropa=form.cleaned_data['tropa'],
            peso_animal=form.cleaned_data['peso_animal'],
        ) 
        animal.save()
        animal.ident='animal:{}-{}'.format(animal.id , animal.tropa)
        animal.save()
        return super(AñadirAnimal , self).form_valid(form)
'''
