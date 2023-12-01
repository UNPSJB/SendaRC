from django.db import models
from core.models import Empleado, Cliente, TipoServicio
from django.utils import timezone
import locale

# Create your models here.

class Servicio(models.Model):
    ESTADO = {
        (1, 'Presupuestado'),
        (2, 'Vencido'),
        (3, 'Contratado'),
        (4, 'En Curso'),
        (5, 'Suspendido'),
        (6, 'Finalizado'),
        (7,'Cancelado'),
    }
    TIPO = {
        (1, 'Eventual'),
        (2, 'Determinado')
    }
    #Datos para presupuestar un servicio
    fecha_emision = models.DateField(auto_now=True, auto_now_add=False)
    plazo_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    direccion = models.CharField(max_length=90)
    metros2 = models.IntegerField()
    observaciones = models.TextField()
    porcentaje = models.IntegerField()
    cant_empleados = models.IntegerField()
    importe_total = models.IntegerField()
    estado = models.PositiveIntegerField(choices=ESTADO)
    tipo = models.PositiveIntegerField(choices=TIPO)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    tipoServicios = models.ManyToManyField(TipoServicio, through='CantServicioTipoServicio')
    #Datos para contratar un servicio
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False, null=True)
    fecha_finaliza = models.DateField(auto_now=False, auto_now_add=False, null=True)
    empleado = models.ManyToManyField(Empleado, null=True) 
    #Otros Datos Adicionales
    fecha_cancelada = models.DateField(auto_now=False, auto_now_add=False, null=True)
    
    def getEstado(self):
        return dict(self.ESTADO)[self.estado]
    
    def getTipo(self):
        return dict(self.TIPO)[self.tipo] 
    
    def getImporteTotalFormateado(self):
        locale.setlocale(locale.LC_ALL, '')  
        return locale.currency(self.importe_total, grouping=True)

class CantServicioTipoServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    
class Frecuencia(models.Model):
    DIA={
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miercoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sabado')
    }
    TURNO={
        (1, 'Mañana'),
        (2, 'Tarde'),
        (3, 'Noche')
    }
    dia = models.PositiveIntegerField(choices=DIA)
    turno = models.PositiveIntegerField(choices=TURNO)
    servicio = models.ForeignKey(Servicio, related_name="frecuencias", on_delete=models.CASCADE)
    empleados = models.ManyToManyField(Empleado, related_name="frecuencias", null=True)
    
    def getHoraInicio(self):
        if self.turno == 1: #Mañana
            return timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)
        elif self.turno == 2: #Tarde
            return timezone.now().replace(hour=14, minute=00, second=0, microsecond=0)
        elif self.turno == 3: #Noche
            return timezone.now().replace(hour=19, minute=00, second=0, microsecond=0)
        
    def getHoraFin():
        if self.turno == 1: #Mañana
            return timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)
        elif self.turno == 2: #Tarde
            return timezone.now().replace(hour=18, minute=00, second=0, microsecond=0)
        elif self.turno == 3: #Noche
            return timezone.now().replace(hour=23, minute=00, second=0, microsecond=0)
        
    @property
    def hora_inicio(self):
        return self.getHoraInicio()
    
    @property
    def hora_fin(self):
        return self.getHoraFin()

class Reclamo(models.Model):
    descripcion = models.CharField(max_length=400)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)

class Asistencia(models.Model):
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    frecuencia = models.ForeignKey(Frecuencia, on_delete=models.DO_NOTHING)
    

