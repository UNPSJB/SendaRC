from django.db import models
from core.models import Empleado, Cliente, TipoServicio, Localidad
from django.utils import timezone


def formato_moneda(valor):
    return (
        "${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    )


class Servicio(models.Model):
    ESTADO = {
        (1, "Presupuestado"),
        (2, "Vencido"),
        (3, "Contratado"),
        (4, "En Curso"),
        (5, "Suspendido"),
        (6, "Finalizado"),
        (7, "Cancelado"),
    }
    TIPO = {(1, "Eventual"), (2, "Determinado")}

    # Datos para presupuestar un servicio
    fecha_emision = models.DateField(auto_now=True, auto_now_add=False)
    plazo_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    direccion = models.CharField(max_length=90)
    metros2 = models.IntegerField()
    observaciones = models.TextField(null=True, blank=True)
    porcentaje = models.IntegerField()
    cant_empleados = models.IntegerField()
    importe_total = models.IntegerField()
    estado = models.PositiveIntegerField(choices=ESTADO)
    tipo = models.PositiveIntegerField(choices=TIPO)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    tipoServicios = models.ManyToManyField(
        TipoServicio, through="CantServicioTipoServicio"
    )

    # Datos para contratar un servicio
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False, null=True)
    fecha_finaliza = models.DateField(auto_now=False, auto_now_add=False, null=True)
    empleado = models.ManyToManyField(Empleado, null=True)

    # Otros Datos Adicionales
    fecha_cancelada = models.DateField(auto_now=False, auto_now_add=False, null=True)
    localidad = models.ForeignKey(
        Localidad, on_delete=models.DO_NOTHING, default=None, null=True
    )

    def __str__(self):
        return self.fecha_emision.strftime("%d/%m/%Y")

    def getEstado(self):
        return dict(self.ESTADO)[self.estado]

    def getTipo(self):
        return dict(self.TIPO)[self.tipo]

    def getLocalidad(self):
        if self.localidad:
            return self.localidad.nombre
        return "No asignada"


    # MÉTODOS PARA EL DESGLOSE DETALLADO DEL PDF

    def getSubtotalPorTurno(self):
        """Subtotal de servicios por un solo turno"""
        servicios_asociados = CantServicioTipoServicio.objects.filter(servicio=self)
        subtotal = sum(
            servicio.tipoServicio.getPrecio(servicio.cantidad)
            for servicio in servicios_asociados
        )
        return subtotal

    def getSubtotalPorTurnoFormateado(self):
        """Subtotal de servicios por turno formateado"""
        return formato_moneda(self.getSubtotalPorTurno())

    def getCantidadFrecuencias(self):
        """Cantidad de frecuencias del servicio"""
        return Frecuencia.objects.filter(servicio=self).count()

    def getTotalServicios(self):
        """Total de servicios considerando todas las frecuencias"""
        return self.getSubtotalPorTurno() * self.getCantidadFrecuencias()

    def getTotalServiciosFormateado(self):
        """Total de servicios formateado"""
        return formato_moneda(self.getTotalServicios())

    def getCantidadEmpleadosCalculados(self):
        """Cantidad de empleados calculados según el tipo de contrato"""
        cant_frecuencias = self.getCantidadFrecuencias()
        if self.tipo == 2:  # Determinado
            return cant_frecuencias * self.cant_empleados * 4
        else:  # Eventual
            return cant_frecuencias * self.cant_empleados

    def getManoObraUnitaria(self):
        """Costo de mano de obra por empleado"""
        try:
            return Empleado.getSueldoBasico() / 24
        except:
            return 120000 / 24  # Valor por defecto

    def getManoObraUnitariaFormateado(self):
        """Costo de mano de obra por empleado formateado"""
        return formato_moneda(self.getManoObraUnitaria())

    def getTotalManoObra(self):
        """Costo total de mano de obra"""
        return self.getManoObraUnitaria() * self.getCantidadEmpleadosCalculados()

    def getTotalManoObraFormateado(self):
        """Costo total de mano de obra formateado"""
        return formato_moneda(self.getTotalManoObra())

    def getGanancia(self):
        """Ganancia del 15% sobre servicios"""
        return 0.15 * self.getTotalServicios()

    def getGananciaFormateado(self):
        """Ganancia formateada"""
        return formato_moneda(self.getGanancia())

    def getImporteBase(self):
        """Importe base antes del ajuste de porcentaje"""
        return 1.15 * self.getTotalServicios() + self.getTotalManoObra()

    def getAjuste(self):
        """Ajuste por porcentaje aplicado"""
        if self.porcentaje != 0:
            return (self.getImporteBase() * self.porcentaje) / 100
        return 0

    def getAjusteFormateado(self):
        """Ajuste formateado"""
        ajuste = self.getAjuste()
        if ajuste != 0:
            return formato_moneda(ajuste)
        return "No aplicado"

    def getImporteTotalFormateado(self):
        """Importe total formateado"""
        return formato_moneda(self.importe_total)

    # MÉTODOS LEGACY (mantener compatibilidad)

    def getImporteTotalServicios(self):
        """Método legacy - usar getTotalServiciosFormateado()"""
        return self.getTotalServiciosFormateado()

    def getSubtotalServiciosFrecuencias(self):
        """Método legacy - usar getTotalServiciosFormateado()"""
        return self.getTotalServiciosFormateado()

    def getSubtotalEmpleados(self):
        """Método legacy - usar getTotalManoObraFormateado()"""
        return self.getTotalManoObraFormateado()

    def getDiasHabilitados(self):
        dias_numeros = self.frecuencias.values_list("dia", flat=True).distinct()
        return [dict(Frecuencia.DIA)[dia] for dia in dias_numeros]



class CantServicioTipoServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def getPrecio(self):
        return self.tipoServicio.precio * self.cantidad

    def getPrecioCantTipoServicio(self):
        return self.tipoServicio.precio * self.cantidad

    def getPrecioCantTipoServicioFormateado(self):
        return formato_moneda(self.getPrecioCantTipoServicio())

    def subTotalPrecio(self):
        sumatoria = int
        sumatoria = sumatoria + self.getPrecio
        return sumatoria


class Frecuencia(models.Model):
    DIA = {
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miercoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sabado"),
    }
    TURNO = {(1, "Mañana"), (2, "Tarde"), (3, "Noche")}
    dia = models.PositiveIntegerField(choices=DIA)
    turno = models.PositiveIntegerField(choices=TURNO)
    servicio = models.ForeignKey(
        Servicio, related_name="frecuencias", on_delete=models.CASCADE
    )
    empleados = models.ManyToManyField(Empleado, related_name="frecuencias", null=True)

    def __str__(self):
        return f"{self.getDia()} - {self.getTurno()}"

    def getDia(self):
        return dict(self.DIA)[self.dia]

    def getTurno(self):
        return dict(self.TURNO)[self.turno]

    def getHoraInicio(self):
        if self.turno == 1:  # Mañana
            return timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)
        elif self.turno == 2:  # Tarde
            return timezone.now().replace(hour=14, minute=00, second=0, microsecond=0)
        elif self.turno == 3:  # Noche
            return timezone.now().replace(hour=19, minute=00, second=0, microsecond=0)

    def getHoraFin():
        if self.turno == 1:  # Mañana
            return timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)
        elif self.turno == 2:  # Tarde
            return timezone.now().replace(hour=18, minute=00, second=0, microsecond=0)
        elif self.turno == 3:  # Noche
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
