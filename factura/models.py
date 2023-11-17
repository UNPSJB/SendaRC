from django.db import *
from core.models import *
from servicio.models import *

# Create your models here.

class Detalle_Factura(models.Model):
    tipo_servicio = models.ForeignKey(Servicio)

class Factura(models.Model):
    FORMAPAGO = {
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Transferencia'),
    }
    importe_total = models.IntegerField()
    fechaemision = models.DateField(auto_now=True, auto_now_add=False)
    formapago =  models.PositiveIntegerField(choices=FORMAPAGO)
    fechapago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    cliente = models.ForeignKey(Cliente)
    servicio = models.ForeignKey(Servicio)
    detalle_tip_servicio = models.ManyToManyField(Detalle_Factura)
    #DETALLES
