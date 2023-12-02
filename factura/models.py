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
    importe = models.IntegerField()
    fechaEmision = models.DateField(auto_now=True, auto_now_add=False)
    formaPago =  models.PositiveIntegerField(choices=FORMAPAGO)
    fechaPago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio,on_delete=models.DO_NOTHING)
    detalle_tip_servicio = models.ManyToManyField(Detalle_Factura)
    #DETALLES
    
class FacturaSeña(models.Model):
    FORMAPAGO = {
        (1, 'Efectivo'),
        (3, 'Transferencia'),
    }
    importe = models.IntegerField()
    fechaEmision = models.DateField(auto_now=True, auto_now_add=False)
    formaPago =  models.PositiveIntegerField(choices=FORMAPAGO)
    fechaPago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio,on_delete=models.DO_NOTHING)
    
