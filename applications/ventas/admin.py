from django.contrib import admin
from .models import Cliente , FacturaDet , FacturaEnc
# Register your models here.

admin.site.register(FacturaEnc)
admin.site.register(FacturaDet)
admin.site.register(Cliente)