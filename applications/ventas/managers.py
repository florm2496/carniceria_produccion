from django.db import models
from django.db.models import Sum


class FacturaEncManager(models.Manager):
    
    def VentasCerradas(self):
        return self.filter(
            cerrada=False
        )
    def TotalVentasCerradas(self):
       return self.filter(
            cerrada=False
        ).aggregate(
            total=Sum('total')
        )
    

class FacturaDetManager(models.Manager): 

    def VentasAnuladas(self):
        return self.filter(
            anulada=True
        )
