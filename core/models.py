from django.db import models

# Create your models here.
class Insumo(models.Model):
    UNIDAD = {
        (1, 'gr'),
        (2, 'Kg'),
        (3, 'ml'),
        (4, 'Lts')
    }
    descripcion = models.CharField(max_length=50)
    unidad_med = models.IntegerField(choices=UNIDAD)
    contenido_neto = models.IntegerField()
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    estado = models.BooleanField(default=True)

    def getInsumo(self):
        return self.insumo.descripcion
    def __str__(self):
        return self.descripcion
    
    def getEstado(self):
        if self.estado == True:
            return "Habilitado"
        else:
            return "Deshabilitado"
    
class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    observaciones = models.TextField()
    activo = models.BooleanField(default=True)
    
class TipoServicio(models.Model):
    UNIDAD = {
        (1, 'm2'),
        (2, 'unidad')
    }
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.PositiveIntegerField(choices=UNIDAD)
    precio = models.IntegerField()
    insumos = models.ManyToManyField(Insumo, through='CantInsumoServicio')
    maquinarias = models.ManyToManyField(Maquinaria)
    activo = models.BooleanField(default=True)
    
    def getPrecio(self, cantidad):
        return self.precio * cantidad
    
class CantInsumoServicio(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(null=True)
    
class Localidad(models.Model):
    cp = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    TIPO = {
        (1, 'Ocacional'),
        (2, 'Habitual'),
    }
    TIPOPERSONA = {
        (1, 'Particular'),
        (2, 'Juridico')
    }
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    tipo = models.PositiveIntegerField(choices=TIPO, default=1)
    tipoPersona = models.PositiveIntegerField(choices=TIPOPERSONA)
    cuil = models.CharField(unique=True,max_length=13)
    telefono =models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)

    def getTipo(self):
        return dict(self.TIPO)[self.tipo]

    def getTipoPersona(self):
        return dict(self.TIPOPERSONA)[self.tipoPersona]

class EmpleadoManager(models.Manager):
    def disponibles(self, desde, dia, turno):
        qdesde = models.Q(frecuencias__servicio__fecha_finaliza__lte=desde)
        qdia = models.Q(frecuencias__dia=dia)
        qturno = models.Q(frecuencias__turno=turno)
        return self.get_queryset().exclude((qdia & qturno) | (~qdia & ~qturno & qdesde))

class Empleado(models.Model):
    numDNI = models.CharField(unique=True,max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    sueldo = models.IntegerField()
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    objects = EmpleadoManager()

    sueldo_basico = 58000
    
    def save(self, *args, **kargs):
        self.sueldo += self.sueldo_basico
        super().save(*args, **kargs)
    
    @classmethod
    def getSueldoBasico(cls):
        return cls.sueldo_basico
    
    
class Sancion(models.Model):
    TIPO = {
        (1, 'Correcion'),
        (2, 'Suspension')
    }
    tipo = models.PositiveIntegerField(choices=TIPO)
    nroSancion = models.IntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    
    def getEmpleado(self):
        return self.empleado.numLegajo