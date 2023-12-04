from django.db import *
from core.models import *
from servicio.models import *

# Create your models here.

class Detalle_Factura(models.Model):
    tipo_servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE)

class Factura(models.Model):
    FORMAPAGO = {
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Transferencia'),
    }
    TIPOFACTURA = {
        (1, 'Seña'),
        (2, 'Unica'),
        (3, 'Mensual')
    }
    tipo = models.PositiveIntegerField(choices=TIPOFACTURA)
    importe = models.IntegerField()
    fechaEmision = models.DateField(auto_now=True, auto_now_add=False)
    formaPago =  models.PositiveIntegerField(choices=FORMAPAGO, null=True)
    fechaPago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio,on_delete=models.DO_NOTHING)
    #DETALLES
    
