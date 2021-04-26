from django.db import models
from applications.bases.models import ClaseModelo


class Unidad(ClaseModelo):
    nombre=models.CharField(max_length=10)
    def __str__(self):
         return self.nombre


MERCADERIA='mercaderia'
CARNE='carne'
TIPO=[
    (MERCADERIA,'mercaderia'),
    (CARNE,'carne'),
]


class Marca(ClaseModelo):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Categoria(ClaseModelo):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
    

class Producto(ClaseModelo):
    nombre=models.CharField(max_length=40)
    descripcion=models.CharField(max_length=100 , blank=True ,null=True)
    codigo=models.CharField(max_length=30 ,unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE ,blank=True,null=True)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE ,blank=True,null=True)
    precioventa=models.FloatField()
    tipo = models.CharField(choices=TIPO, max_length=50 , blank=True ,null=True)
    unidad=models.ForeignKey(Unidad, on_delete=models.CASCADE)
    existencia=models.IntegerField(default=0)
    ultimacompra=models.DateField(blank=True , null=True)
    
    
    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        

    def __str__(self):
            return '{} - {}'.format(self.nombre,self.tipo)




  
