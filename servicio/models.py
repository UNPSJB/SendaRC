from django.db import models
from core.models import Empleado, Cliente, TipoServicio
from django.utils import timezone
import locale

# Create your models here.
locale.setlocale(locale.LC_ALL, '') 

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
    
    def getImporteTotalServicios(self):
        servicios_asociados = CantServicioTipoServicio.objects.filter(servicio=self)
        total_importe = sum(servicio.tipoServicio.precio * servicio.cantidad for servicio in servicios_asociados)

        return locale.currency(total_importe, grouping=True)

    def getSubtotalServiciosFrecuencias(self):
        servicios_asociados = CantServicioTipoServicio.objects.filter(servicio=self)
        total_servicios = sum(servicio.tipoServicio.precio * servicio.cantidad for servicio in servicios_asociados)
        subtotal_servicios =  total_servicios * len(Frecuencia.objects.filter(servicio=self))
        return locale.currency(subtotal_servicios, grouping=True)
    
    def getSubtotalEmpleados(self):
        mano_obra = Empleado.getSueldoBasico() / 24
        if self.tipo == 'Determinado':
            cant_empleados = len(Frecuencia.objects.filter(servicio=self)) * self.cant_empleados *  4      #El 4 es por el mes tiene cuatro semanas
        else:
            cant_empleados = len(Frecuencia.objects.filter(servicio=self)) * self.cant_empleados 
        
        subtotal = mano_obra * cant_empleados
        return locale.currency(subtotal, grouping=True)

    def getImporteTotalFormateado(self):
        return locale.currency(self.importe_total, grouping=True)

class CantServicioTipoServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def getPrecio(self):
        return self.tipoServicio.precio * self.cantidad
    
    def subTotalPrecio(self):
        sumatoria = int
        sumatoria = sumatoria + self.getPrecio 
        return sumatoria
    

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
    
    def getDia(self):
        return dict(self.DIA)[self.dia]
    
    def getTurno(self):
        return dict(self.TURNO)[self.turno]
    
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