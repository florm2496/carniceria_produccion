from django.shortcuts import render ,redirect
from .models import Cliente , FacturaDet ,FacturaEnc
from django.views import generic
from .forms import ClienteForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
from applications.productos.models import Producto
from django.contrib.auth.decorators import login_required, permission_required
from applications.bases.views import SinPrivilegios
from django.contrib.auth import authenticate
from .models import FacturaDet , FacturaEnc
#from applications.carne.models import Cortes
# Create your views here.

class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Cliente creado exitosamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Cliente modificado exitosamente"

    def form_valid(self, form):
        #form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate,SinPrivilegios):
    model=Cliente
    template_name="ventas/nuevo_cliente.html"
    form_class=ClienteForm
    success_url= reverse_lazy("ventas:lista_clientes")
    permission_required='ventas.add_cliente'
    success_message='Cliente creado exitosamente'
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    
class ClienteList(SinPrivilegios,generic.ListView):
    model = Cliente
    template_name = "ventas/lista_clientes.html"
    context_object_name = "obj"
    permission_required='ventas.view_cliente'

    def get_queryset(self):
        return super().get_queryset().filter(~Q(nombre='casual'))
    
  

class ClienteEdit(VistaBaseEdit,SinPrivilegios):
    model=Cliente
    template_name="ventas/nuevo_cliente.html"
    form_class=ClienteForm
    success_url= reverse_lazy("ventas:lista_clientes")
    permission_required='ventas.update_cliente'
    success_message='Cliente actualizado exitosamente'

    

#VISTA DE FUNCIONES
@login_required(login_url="/login/")
@permission_required("ventas.view_facturaenc",login_url="bases:sin_privilegios")

def Ventas(request , id=None):
    template_name='ventas/nueva_venta.html'
    encabezado={
        'fecha':datetime.today()
    }
    detalle={}
    
    clientes=Cliente.objects.filter(estado=True)
    

    if request.method=='GET':
        enc=FacturaEnc.objects.filter(pk=id).first()
        if not enc:
            encabezado={
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00 ,
                'descuento':0.00 ,
                'total': 0.00
        
            }
            detalle=None
        else:
            encabezado={
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total


            }
          



        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}
        return render(request,template_name,contexto)

    if request.method=='POST':
        cliente=request.POST.get("enc_cliente")
      
        fecha=request.POST.get("enc_fecha")
        cli=Cliente.objects.get(pk=cliente)
      

        if not id:
            enc=FacturaEnc(
                cliente=cli,
                fecha=fecha,
                uc=request.user

            )
            if enc:
                enc.save()
                id=enc.id
        else:
            enc=FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente=cli
                enc.save()
        if not id:
            messages.error(request , "No se puede continuar ,Numero de factura no detectado")
            return redirect("ventas:ventas")

        codigo=request.POST.get("codigo")
        cantidad=request.POST.get("cantidad")
        precio=request.POST.get("precio")
        s_total=request.POST.get("sub_total_detalle")
        descuento=request.POST.get("descuento_detalle")
        total=request.POST.get("total")

        prod=Producto.objects.get(codigo=codigo)


        det=FacturaDet(
            factura=enc,
            producto=prod,
            cantidad=cantidad,
            precio=precio,
            sub_total=s_total,
            descuento=descuento,
            total=total,
            uc=request.user
            )
        if det:
            det.save()
        return redirect('ventas:editar_venta',id=id)



    return render(request , template_name, contexto)


class EncVentaList(SinPrivilegios,generic.ListView):
    model = FacturaEnc
    context_object_name='obj'
    template_name = "ventas/lista_ventas.html"
    permission_required='ventas.view_facturaenc'
    facs=FacturaEnc.objects.values('fecha')


def ListaProductosTablaVenta(request):
    template_name='ventas/tabla_productos.html'
    context={ 
        'productos':Producto.objects.all().order_by('tipo')  ##este order by devuelve primero los productos tipo carne y
        }                                                      #y luego la mercaderia
    return render(request,template_name,context)




############################################################################################################
def borrar_detalle_factura(request, id):
    template_name = "ventas/borrar_detalle.html"
    det = FacturaDet.objects.get(pk=id)
    
  
    #obteniendo la factura que se relaciona con este detalle
    id_enc=det.factura.id
    #obteniendo una instancia de esa factura
    enc=FacturaEnc.objects.get(pk=id_enc)
    
    #obteniendo el cliente de esa factura
    cliente=enc.cliente

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("ventas.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()
            
            cantidad_descontada=det.sub_total
            saldo=cliente.saldo

            if saldo!=float(0):
                
                cliente.saldo=saldo+cantidad_descontada
                cliente.save()
                print('------------------------se hizo el descuento')
            elif saldo==float(0):

                print('el saldo ya es 0',cliente.saldo)
            

            
            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)

'''

            #se obtiene el cliente que relacionado a la venta(o el que realizo la compra)
            cliente_id=enc.cliente.id
            #se obtiene la instancia de ese cliente
            cliente=Cliente.objects.get(pk=cliente_id)
            #se obtiene el saldo que tenia el cliente antes de realizar la compra
            saldo=cliente.saldo
            print('desde el borrado',enc.sub_total)
            #se actualiza su saldo con el monto de la compra que realizo
            cliente.saldo=saldo + enc.sub_total
            #se guarda la actualizacion en la base de datos
            cliente.save()'''