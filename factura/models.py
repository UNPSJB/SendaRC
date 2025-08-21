from django.db import models
from core.models import *
from servicio.models import *

# Create your models here.  

    
class Factura(models.Model):
    FORMAPAGO = {
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Transferencia'),
    }
    TIPOFACTURA = {
        (1, 'Seña'),
        (2, 'Unica'),
        (3, 'Mensual'),
    }
    tipo = models.PositiveIntegerField(choices=TIPOFACTURA)
    importe = models.IntegerField()
    fechaEmision = models.DateField(auto_now=False, auto_now_add=False)
    fecha_vencimiento = models.DateField(auto_now=False, auto_now_add=False, null=True)
    periodoServicio = models.IntegerField(null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio,on_delete=models.DO_NOTHING)
    periodo = models.CharField(max_length=7, null=True)
    # Atributos para el pago
    formaPago =  models.PositiveIntegerField(choices=FORMAPAGO, null=True)
    fechaPago = models.DateField(auto_now=False, auto_now_add=False, null=True)
    
    
    def getImporteFormateado(self):
            return f"${self.importe:,.0f}".replace(",", ".")
    
    def getTipo(self):
        return dict(self.TIPOFACTURA)[self.tipo] 
    
    def getFormaPago(self):
        return dict(self.FORMAPAGO)[self.formaPago]
    
    def getPeriodoServicio(self):
        meses = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre',
            13: 'Un Dia'
        }
        return meses.get(self.periodoServicio, 'Mes no válido')

    
    
class Detalle_Servicios(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    tipo_servicio = models.CharField(max_length=50)
    tipo_servicio_Unit = models.CharField(max_length=50)
    precio_tipo_servicio = models.IntegerField()
    cantidad = models.IntegerField()


class Detalle_Empleados(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cantidad_empleados = models.IntegerField()
    #Importe que crabamos por mano de obra por la todos los empleados que trabajan en el servicio, eventual=un dia, determinado=un mes
    importe_mano_obra = models.IntegerField()

    def getImporteManoObraFormateado(self):
        return f"${self.importe_mano_obra:,.0f}".replace(",", ".")
    
