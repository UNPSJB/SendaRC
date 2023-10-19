from django.db import models

# Create your models here.
class Insumo(models.Model):
    UNIDAD = {
        (1, 'gr'),
        (2, 'Kg'),
        (3, 'ml'),
        (4, 'Lts')
    }
    codigo = models.IntegerField(auto_created=True, primary_key=True)
    descripcion = models.CharField(max_length=50)
    unidad_med = models.IntegerField(choices=UNIDAD)
    contenido_neto = models.IntegerField()
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    
class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    observaciones = models.TextField()
    baja = models.BooleanField()
    
class TipoServicio(models.Model):
    UNIDAD = {
        (1, 'm2'),
        (2, 'unidad')
    }
    codigo = models.IntegerField(auto_created=True, primary_key=True)
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.PositiveIntegerField(choices=UNIDAD)
    precio = models.IntegerField()
    insumos = models.ManyToManyField(Insumo, through='CantInsumoServicio')
    maquinarias = models.ManyToManyField(Maquinaria)
    
class CantInsumoServicio(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(null=True)
    
class Localidad(models.Model):
    cp = models.IntegerField(primary_key=True)
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
    tipo = models.PositiveIntegerField(choices=TIPO)
    tipoPersona = models.PositiveIntegerField(choices=TIPOPERSONA)
    cuil = models.IntegerField(primary_key=True)
    telefono = models.IntegerField()
    email = models.EmailField(max_length=254)
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)

    def getTipo(self):
        return dict(self.TIPO)[self.tipo]

    def getTipoPersona(self):
        return dict(self.TIPOPERSONA)[self.tipoPersona]

class Empleado(models.Model):
    numDNI = models.IntegerField(primary_key=True)
    numLegajo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    email = models.EmailField(max_length=254)
    sueldo = models.IntegerField()
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)
    
class Sancion(models.Model):
    TIPO = {
        (1, 'Correcion'),
        (2, 'Suspension')
    }
    tipo = models.PositiveIntegerField(choices=TIPO)
    nroSancion = models.IntegerField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    
    def getEmpleado(self):
        return self.empleado.numLegajo
    
  

