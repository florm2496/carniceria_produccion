from django.contrib import admin

# Register your models here.
from .models import Caja,MovimientosCaja,Concepto
#,CierreCaja

admin.site.register(Caja)
admin.site.register(MovimientosCaja)
admin.site.register(Concepto)
#admin.site.register(CierreCaja)