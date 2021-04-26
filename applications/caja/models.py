from django.db import models
from applications.bases.models import ClaseModelo
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .managers import CierreCajaManager


tipo_movimiento=[
    ('EGRESO','egreso'),
    ('INGRESO','ingreso'),
]
 
class Caja(ClaseModelo):
    monto_inicial=models.FloatField(default=0)
    monto_actual=models.FloatField(default=0)
    ultima_apertura=models.DateTimeField(auto_now=True)
    ultimo_cierre=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cajas"
        verbose_name="Caja"

    def __str__(self):
        return str(self.monto_actual)

class Concepto(ClaseModelo):
    nombre=models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class MovimientosCaja(ClaseModelo):
    monto=models.FloatField(default=0)
    movimiento=models.CharField(max_length=20 , choices=tipo_movimiento,default='EGRESO')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE ,blank=True,null=True)
    observacion = models.CharField(max_length=50)
    #caja=models.ForeignKey(Caja , on_delete=models.CASCADE ,default=0)

    class Meta:
        verbose_name_plural = "Movimientos"
        verbose_name="Movimiento"

    def __str__(self):
        return str(self.monto) + self.movimiento



    

@receiver(post_save ,sender=MovimientosCaja)

def monto_caja(sender ,instance , **kwargs):
    
    monto_mov=instance.monto
    monto_caja=Caja.objects.last()
    print(monto_mov ,monto_caja)
    if instance.movimiento=='EGRESO':
        monto_caja.monto_actual=monto_caja.monto_actual-monto_mov
        print('----------',monto_caja.monto_actual)
        monto_caja.save()
    elif instance.movimiento=='INGRESO':
        monto_caja.monto_actual=monto_caja.monto_actual+monto_mov
        print('-------',monto_caja.monto_actual)
        monto_caja.save()



'''

def save(self , *args , **kwargs):
        monto_actual_caja=self.caja.monto_actual
        self.caja.monto_actual= monto_actual_caja+self.monto_ingreso
        super(Ingreso,self).save(*args,**kwargs)

   def save(self , *args , **kwargs):
        monto_actual_caja=self.caja.monto_actual
        self.caja.monto_actual= monto_actual_caja-self.monto_egreso
        super(Egreso,self).save(*args,**kwargs)



        '''