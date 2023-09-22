from django.db import models

# Create your models here.
class Insumo(models.Model):
    UNIDAD = {
        (1, 'm2'),
        (2, 'unidad')
    }
    codigo = models.IntegerField()
    descripcion = models.TextField()
    unidad_med = models.PositiveIntegerField(choices=UNIDAD)
    contenido_neto = models.IntegerField()
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    
class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50)
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
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.PositiveIntegerField(choices=UNIDAD)
    precio = models.IntegerField()
    insumos = models.ManyToManyField(Insumo)
    maquinarias = models.ManyToManyField(Maquinaria)
    
class CantInsumoServicio(models.Model):
    cantidad = models.IntegerField()
    insumo = models.ForeignKey(Insumo, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    
class Localidad(models.Model):
    cd = models.IntegerField()
    nombre = models.CharField(max_length=100)

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
    tipo = models.PositiveIntegerField(choices=TIPO)
    tipopersona = models.PositiveIntegerField(choices=TIPO)
    cuil = models.IntegerField()
    telefono = models.IntegerField()
    email = models.EmailField(max_length=254)
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING)

class Empleado(models.Model):
    numdocumento = models.IntegerField()
    numlegajo = models.IntegerField()
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
    nroSancion = models.IntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING)
    
  

