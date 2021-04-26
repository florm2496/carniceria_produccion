from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
# Create your models here.
from applications.bases.models import ClaseModelo
from applications.caja.models import Caja
from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from applications.productos.models import Producto
from applications.ventas.managers import FacturaDetManager,FacturaEncManager




class Cliente(ClaseModelo):
    nombre = models.CharField(max_length=50, default='casual')
    saldo=models.FloatField(default=0)
    numero = models.CharField(blank=True,null=True, max_length=50)
    direccion = models.CharField(blank=True,null=True, max_length=50)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural='Clientes'

class FacturaEnc(ClaseModelo):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    cerrada=models.BooleanField(default=False)
    objects=FacturaEncManager()

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
    #3    permissions = [
      #      ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
       # ]
    
#venta anulada= es aquella venta que se cancela
#venta cerrada=es aquella venta que se cierra en un cierre de caja 

class FacturaDet(ClaseModelo):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.FloatField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    anulada=models.BooleanField(default=False)
    objects=FacturaDetManager()

    def __str__(self):
        return '{} - {}'.format(self.producto,self.sub_total) 

    def save(self):
        self.sub_total = float(float(float(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
    #    permissions = [
     #       ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
      #  ]

        

      
@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    enc = FacturaEnc.objects.get(pk=factura_id)
    
    detalle=FacturaDet.objects.get(pk=instance.id)
    subtotal=detalle.sub_total
    #print('detalle del subtotal',detalle.sub_total)

    if enc:
        sub_total = FacturaDet.objects.filter(factura=factura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total',0.00)

        print(FacturaDet.objects.filter(factura=factura_id))

        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        

        enc.sub_total = sub_total
        #print('///////////////////',enc.sub_total)
        enc.descuento = descuento

        enc.save()

        cliente=enc.cliente
        saldo=cliente.saldo
        if subtotal>=0:
            cliente.saldo=saldo + subtotal
            cliente.save()
            print('saldo del cliente positivo')
        elif subtotal<0:
            print('saldo cliente ngativo',cliente.saldo)
        
        

    producto=Producto.objects.filter(pk=producto_id).first()
    
    if producto:
        if producto.tipo=='MERCADERIA' or producto.tipo=='mercaderia':
            if int(producto.existencia) >= int(instance.cantidad):
                cantidad = int(producto.existencia) - int(instance.cantidad)
                producto.existencia = cantidad
                producto.save()
                print('GHJJJJJJJJo')
            else:
                print('no hay stock')
        elif producto.tipo=='CARNE' or producto.tipo=='carne':
            print('if carne')
            #cantidad vendida del corte de carne en esta instancia de venta
            cantidad_vendida=float(instance.cantidad)
            #se tratara al campo existencia del corte como la cantidad vendida en total
            ventas_actual_corte=float(producto.existencia)
            if cantidad_vendida>0:
                print('******')
                producto.existencia= ventas_actual_corte + cantidad_vendida
                producto.save()

            elif (cantidad_vendida<0):
                print('descontar cantidad vendida porque s eborro la venta ')
                #antes se debe verificar que la cantidad vendida sea mayor a la cantidad que se esta por descontar asi no
                # se producen valores negativos
                cantidad_positiva=float(instance.cantidad) * -1
                if float(producto.existencia) >= cantidad_positiva :
                    producto.existencia= ventas_actual_corte + cantidad_vendida
                    producto.save()
                else: 
                    print('no hacer nada')

                
            print('el producto era de tipo' , producto.tipo , 'no se deconto el stock')






@receiver(post_save, sender=FacturaDet)

def ventas_caja(sender ,instance , **kwargs):
    ultima_venta=FacturaDet.objects.last()
    ultimo_total=ultima_venta.total
    caja=Caja.objects.last()
    monto_actual_caja=caja.monto_actual
    #print('caja ahora' , monto_actual_caja)
    caja.monto_actual=monto_actual_caja+ultimo_total
    caja.save()
    #print('caja luego de sumar',ultimo_total,':',caja.monto_actual)


'''
@receiver(post_save, sender=Pago)
def realizar_pago(sender,instance,**kwargs):
    
    
    
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
        cliente.save()

    
    
    
    
    
    
    
    '''