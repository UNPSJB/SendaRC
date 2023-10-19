from django.db import models

# Create your models here.

class factura(models.Model):
    FORMAPAGO = {
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Transferencia'),
    }
    importetotal = models.IntegerField()
    fechaemision = models.DateField(auto_now=True, auto_now_add=False)
    formapago =  models.PositiveIntegerField(choices=FORMAPAGO)
    fechapago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    #DETALLES
