from django.contrib import admin
from .models import Unidad,Producto,Categoria,Marca
# Register your models here.

admin.site.register(Producto)

admin.site.register(Unidad)
admin.site.register(Categoria)
admin.site.register(Marca)