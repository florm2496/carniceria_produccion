from django.db import models
from applications.bases.models import ClaseModelo
from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.ventas.models import Cliente
from django.db.models import Sum
# Create your models here.


#######################################################################
class Tropa(ClaseModelo):
    cant_animales = models.IntegerField()


    def __str__(self):
        return 'Tropa numero'+str(self.id)

##############################################################################    

class Animal(ClaseModelo):
    numero=models.IntegerField(default=0)
    ident=models.CharField(max_length=50,blank=True, null=True)
    tropa = models.ForeignKey(Tropa, on_delete=models.CASCADE)
    peso_animal=models.FloatField(default=0)

    #def save(self):
        #self.ident='animal:{}-tropa:{}'.format(self.id ,self.tropa)
     #   super(Animal , self).save()

    def __str__(self):
        #aqui deberia retornar el identificador del animal ?
        return 'Animal'+ str(self.numero) +'-'+ str(self.tropa)
    

#################################################################################################

class Res(ClaseModelo):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    nombre=models.CharField(default='Res' ,max_length=20)
    peso= models.FloatField(max_length=7 , default=0)
    ingreso = models.DateTimeField(auto_now_add=True)
    vendida=models.BooleanField(default=False)
    
   

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Res'
        verbose_name_plural = 'Reses'

    def __str__(self):
        return self.nombre 

#################################viejo modelo de ventas###########################################################################

class EncVentaReses(ClaseModelo):
    fecha = models.DateTimeField(auto_now_add=True , blank=True ,null=True)
    total = models.FloatField(default=0.0)
    cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #me sirve o no tener este campo??
    saldada=models.BooleanField(default=True) #porque la mayoria de las ventas seran de contado
    observacion = models.TextField(max_length=40,blank=True ,null=True)  
    #pagos = models.ForeignKey(Prueba,on_delete=models.CASCADE ,blank=True ,null=True) 

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'EncVentaReses'
        verbose_name_plural = 'EncsVentaReses'

class DetalleVentaRes(ClaseModelo):
    #venta -> venta a la cual pertenece un detalle de venta. en el modelo de arriba se llama enc
    venta=models.ForeignKey(EncVentaReses,on_delete=models.CASCADE,blank=True,null=True)
    res=models.ForeignKey(Res, on_delete=models.CASCADE)
    subtotal=models.FloatField(default=0)
    precio = models.FloatField(default=0.0,blank=True,null=True)

    class Meta:
        verbose_name = 'DetalleVentaRes'
        verbose_name_plural = 'DetallesVentaReses'
########################################################################################



class MedioPago(ClaseModelo):
    nombre=models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name='Medio de pago'
        verbose_name_plural='Medios de pago'

##################################################################################################        

class PagoReses(ClaseModelo):
    monto = models.FloatField(default=0.0)
    medio = models.ForeignKey(MedioPago, on_delete=models.CASCADE , blank=True ,null=True)
    venta = models.ForeignKey(EncVentaReses, on_delete=models.CASCADE,blank=True ,null=True)

    class Meta:
        

        verbose_name = 'pago_res'
        verbose_name_plural = 'pagos_reses'

    def __str__(self):
        
        return str(self.monto)
########################################################################################################
class PagoCliente(ClaseModelo):
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE ,blank=True,null=True)
    monto = models.FloatField(default=0.0)
    medio = models.ForeignKey(MedioPago, on_delete=models.CASCADE , blank=True ,null=True)
    class Meta:
    
        verbose_name = 'pago_cliente'
        verbose_name_plural = 'pagos_clientes'

    def __str__(self):
        
        return str(self.monto)



#SECCION DE SIGNALS


@receiver(post_save, sender=Animal)
def CrearResesDeUnAnimal(sender, instance,**kwargs):
    tropa=instance.tropa            #ESTO DEBERIA ESTAR EN OTRO PROCESO
    id_animal=instance.id
   
    animal=Animal.objects.filter(id=id_animal).update(
        ident='animal{}-{}'.format(id_animal,tropa),
    )
   
    #print('desde el signal',animal) la variable animal devuelve 1 , esto quiere decir que el update fue exitoso
   
    #PROCESO PARA CREAR LAS DOS MEDIA RESES PERTENECIENTES  AL ANIMAL EN CUESTION
    reses=[]
    anm=Animal.objects.get(id=id_animal)
    for num in range(2):
        res =Res(
            animal=anm,             #aqui se deberia pasar el numero y no el id del animal
            nombre='res{}-animal{}'.format(num,anm.numero),
        )
        reses.append(res)
    Res.objects.bulk_create(reses)

#este signal es para cambiar el estado de una res luego de que se vende
@receiver(post_save, sender=DetalleVentaRes)
def post_venta_res(sender , instance,**kwargs):
    #venta a la cual pertence este detalle
    venta=instance.venta.id
    #obtengo la instancia de la res vendida
    id_res=instance.res.id
    res=Res.objects.get(pk=id_res)
    res.vendida=True
    res.save()


    enc=EncVentaReses.objects.filter(pk=venta).first()
    if enc:
        subtotal=DetalleVentaRes.objects.filter(venta=venta).aggregate(subtotal=Sum('subtotal')).get('subtotal',0.00)

        enc.total=subtotal

        enc.save()

        #actualizar saldo del cliente con una nueva venta. no comtempla el borrado
        cliente_id=enc.cliente.id
        cliente=Cliente.objects.get(pk=cliente_id)
        saldo_actual=cliente.saldo

        if subtotal>=0:
            cliente.saldo=saldo_actual + subtotal
            cliente.save()
            print('saldo del cliente positivo')
        elif subtotal<0:
            print('saldo cliente ngativo',cliente.saldo)

@receiver(post_save, sender=PagoCliente)       
def post_pago_clientes(sender , instance,**kwargs):
    cliente_pago=instance.cliente
    cliente=Cliente.objects.get(pk=cliente_pago.id)
    saldo_actual=cliente.saldo
    monto=instance.monto

    if saldo_actual>=monto:
        cliente.saldo=saldo_actual-monto
        cliente.save()
        print('nuevo saldo del cliente {} luego de descontar {}'.format(cliente.saldo,instance.monto))

    




    '''
    
class Prueba(models.Model):
    monto = models.CharField(max_length=50)
    medio = models.CharField(max_length=50)
    venta = models.ForeignKey(EncVentaReses, on_delete=models.CASCADE,blank=True ,null=True)

    def __str__(self):
        return self.monto + self.medio

    class Meta:
        verbose_name = 'prueba'
        verbose_name_plural = 'pruebas'



        
#este metodo luego de realizar una venta de reses , cambia el estado de la res vendida a True


#@receiver(post_save, sender=VentaReses)
def vender_reses(sender , instance,**kwargs):
    #obtener id de la res vendida
    id_res=instance.res.id
    #obtener la instancia de la res
    res=Res.objects.get(pk=id_res)
    #cambiar estado de la res
    res.vendida=True
    res.save()
    #aumentar monto de la venta al saldo del cliente
    id_cliente=instance.cliente.id

    cliente=Cliente.objects.get(pk=id_cliente)

    saldo_cliente=cliente.saldo
    print('desde el signal')
    precio_venta=instance.precio

    cliente.saldo=saldo_cliente+precio_venta

    #si se da de baja la venta con el estado=True
    if instance.estado is True:
        cliente.saldo=saldo_cliente-precio_venta

    cliente.save()




    @receiver(post_save, sender=PagoReses)
def pago_res(sender , instance,**kwargs):
    venta_id=instance.venta.id
    venta=EncVentaReses.objects.get(pk=venta_id)
    #cliente relacionado a la venta
    cliente=venta.cliente
    #obtener instancia de cliente
    instancia_cliente=Cliente.objects.get(nombre=cliente)
    
    #total de la venta
    
    if str(instance.medio)=='FIADO':
        monto_pago=float(instance.monto)
        saldo_cliente=instancia_cliente.saldo
        instancia_cliente.saldo=saldo_cliente+monto_pago
        print(monto_pago,instancia_cliente.saldo)
        instancia_cliente.save()
        print(instancia_cliente.saldo)

'''


