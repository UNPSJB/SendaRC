from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


def formato_moneda(valor):
    return (
        "${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    )


class InsumoManager(models.Manager):
    def __init__(self, habilitado=None, *qargs, **kwargs):
        super().__init__(*qargs, **kwargs)
        self.habilitado = habilitado

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(activo=self.habilitado) if self.habilitado is not None else qs


class ClienteManager(models.Manager):
    def __init__(self, activo=None, *qargs, **kwargs):
        super().__init__(*qargs, **kwargs)
        self.activo = activo

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(activo=self.activo) if self.activo is not None else qs


class MaquinariaManager(models.Manager):
    def __init__(self, activo=None, *qargs, **kwargs):
        super().__init__(*qargs, **kwargs)
        self.activo = activo

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(activo=self.activo) if self.activo is not None else qs


class InsumoQuerySet(models.QuerySet):
    pass


class TipoServicioManager(models.Manager):
    def __init__(self, activo=None, *qargs, **kwargs):
        super().__init__(*qargs, **kwargs)
        self.activo = activo

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(activo=self.activo) if self.activo is not None else qs


# Create your models here.
class Insumo(models.Model):
    UNIDAD = {(1, "gr"), (2, "Kg"), (3, "ml"), (4, "Lts")}
    descripcion = models.CharField(max_length=50)
    unidad_med = models.IntegerField(choices=UNIDAD)
    contenido_neto = models.IntegerField()
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=True)
    objects = InsumoManager()
    habilitados = InsumoManager(True)
    deshabilitados = InsumoManager(False)

    def getInsumo(self):
        return self.insumo.descripcion

    def __str__(self):
        return f"{self.descripcion} - ({self.marca})"

    def getEstado(self):
        if self.activo == True:
            return "Habilitado"
        else:
            return "Deshabilitado"

    def getUni_Medida(self):
        return dict(self.UNIDAD).get(self.unidad_med, "")


class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    observaciones = models.TextField()
    activo = models.BooleanField(default=True)
    objects = MaquinariaManager()
    habilitadas = MaquinariaManager(True)
    deshabilitadas = MaquinariaManager(False)

    def __str__(self):
        return f"{self.nombre} - {self.modelo} ({self.marca})"


class TipoServicio(models.Model):
    UNIDAD = {(1, "m2"), (2, "unidad")}
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.PositiveIntegerField(choices=UNIDAD)
    precio = models.IntegerField()
    insumos = models.ManyToManyField(Insumo, through="CantInsumoServicio")
    maquinarias = models.ManyToManyField(Maquinaria, null=True)
    activo = models.BooleanField(default=True)
    objects = TipoServicioManager()
    habilitados = TipoServicioManager(True)
    deshabilitados = TipoServicioManager(False)

    def getUnidadMedida(self):
        return dict(self.UNIDAD)[self.unidad_medida]

    def getPrecioFormateado(self):
        return "${:,.2f}".format(self.precio)

    def getPrecio(self, cantidad):
        return self.precio * cantidad
    


class CantInsumoServicio(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)


class Localidad(models.Model):
    cp = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    TIPO = {
        (1, "Ocacional"),
        (2, "Habitual"),
    }
    TIPOPERSONA = {(1, "Particular"), (2, "Juridico")}
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    tipo = models.PositiveIntegerField(choices=TIPO, default=1)
    tipoPersona = models.PositiveIntegerField(choices=TIPOPERSONA)
    cuil = models.CharField(unique=True, max_length=13)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    objects = ClienteManager()
    habilitados = ClienteManager(True)
    deshabilitados = ClienteManager(False)

    def getTipo(self):
        return dict(self.TIPO)[self.tipo]

    def __str__(self):
        return self.nombre + " " + self.apellido

    def getTipoPersona(self):
        return dict(self.TIPOPERSONA)[self.tipoPersona]


class EmpleadoManager(models.Manager):
    def __init__(self, habilitado=None, *qargs, **kwargs):
        super().__init__(*qargs, **kwargs)
        self.habilitado = habilitado

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(activo=self.habilitado) if self.habilitado is not None else qs

    def disponibles(self, desde, hasta, dia, turno):
        qfin = models.Q(frecuencias__servicio__fecha_finaliza__lt=desde)
        qinicio = models.Q(frecuencias__servicio__fecha_inicio__gt=hasta)
        qdia = models.Q(frecuencias__dia=dia)
        qturno = models.Q(frecuencias__turno=turno)

        empleados = self.get_queryset()

        # Esto te muestra qué empleados están ocupados en el mismo día y turno
        ocupados = empleados.filter(
            frecuencias__dia=dia,
            frecuencias__turno=turno,
            frecuencias__servicio__fecha_inicio__lte=hasta,
            frecuencias__servicio__fecha_finaliza__gte=desde,
        ).distinct()

        print("\n--- EMPLEADOS OCUPADOS en misma frecuencia ---")
        for o in ocupados:
            print(f"{o.nombre} {o.apellido} (id={o.id})")

        disponibles = empleados.exclude(id__in=ocupados)
        return disponibles


class Empleado(models.Model):
    numDNI = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    sueldo = models.IntegerField()
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    sueldo_basico = 58000
    objects = EmpleadoManager()
    habilitados = EmpleadoManager(True)
    deshabilitados = EmpleadoManager(False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.pk:  # Solo si es un objeto nuevo
            self.sueldo += self.sueldo_basico
        super().save(*args, **kwargs)

    @classmethod
    def getSueldoBasico(cls):
        return cls.sueldo_basico

    def getEstado(self):
        if self.activo == True:
            return "Habilitado"
        else:
            return "Deshabilitado"

    def getSueldoFormateado(self):
        return formato_moneda(self.sueldo)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    def correccionesAnuales(self):
        return self.sancion_set.filter(tipo=1, fecha_sancion__year = timezone.now().year).count()

class Sancion(models.Model):
    TIPO = {
        (1, 'Correcion'),
        (2, 'Suspension')
    }
    tipo = models.PositiveIntegerField(choices=TIPO)
    nroSancion = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    fecha_sancion = models.DateField(default=timezone.now)
    descripcion = models.TextField()
    diasSuspension = models.PositiveIntegerField(default=0, blank=True)
    
    def getDNIEmpleado(self):
        return self.empleado.numDNI

    def getNombreEmpleado(self):
        return f"{self.empleado.nombre} {self.empleado.apellido}"

    def getTipo(self):
        return dict(self.TIPO)[self.tipo]

    def getFechaFinSancion(self):
        return self.fecha_sancion + timedelta(days=self.diasSuspension)
    
    def getEstadoSuspencion(self):
        if self.getFechaFinSancion() < timezone.now().date():
            return "Vencida"
        else:
            return "Vigente"