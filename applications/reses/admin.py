from django.contrib import admin

# Register your models here.
from .models import Tropa,Animal,Res,EncVentaReses,DetalleVentaRes,PagoReses,MedioPago,PagoCliente


admin.site.register(Tropa)
admin.site.register(Animal)
admin.site.register(Res)
admin.site.register(EncVentaReses)
admin.site.register(DetalleVentaRes)
admin.site.register(PagoReses)
admin.site.register(MedioPago)
admin.site.register(PagoCliente)