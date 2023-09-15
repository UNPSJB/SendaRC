from django.db import models

# Create your models here.

class servicio(models.Model):
    ESTADO = {
        (1, 'Presupuestodo'),
        (2, 'Contratado'),
        (3, 'Finalizado'),
        (4,'Cancelado'),
    }
    nro_servicio = models.AutoField(primary_key=True)
    fecha_emision = models.DateField(auto_now=True, auto_now_add=False)
    plazo_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    direccion = models.CharField(max_length=90)
    metros2 = models.IntegerField()
    observaciones = models.TextField()
    porcentaje = models.IntegerField()
    cant_empleados = models.IntegerField()
    importe_total = models.IntegerField()
    estado = models.PositiveIntegerField(choices=TIPO)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_finaliza = models.DateField(auto_now=False, auto_now_add=False)
    fecha_cancelada = models.DateField(auto_now=False, auto_now_add=False)
    #Empleados = models.ManytoMany
    #Frecuencia = ForeaignKey
    #CLIENTE

class tipoServicio(models.Model):
    UNIDAD = {
        (1, 'm2'),
        (2, 'unidad')
    }
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.PositiveIntegerField(choices=UNIDAD)
    precio = models.IntegerField()
    #INSUMO
    #MAQUINARIA

class insumo(models.Model):
    UNIDAD = {
        (1, 'm2'),
        (2, 'unidad')
    }
    codigo = models.IntegerField()
    descripcion = models.TextField()
    unidad_med = models.PositiveIntegerField(choices=UNIDADES)
    contenido_neto = models.IntegerField()
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()

class maquinaria(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    observaciones = models.TextField()
    baja = models.BooleanField()

class cliente(models.model):
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
    

class empleado(models.Model):
    numdocumento = models.IntegerField()
    numlegajo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    email = models.EmailField(max_length=254)
    sueldo = models.IntegerField()
    #SANCION
