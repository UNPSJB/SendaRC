from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from servicio.models import Servicio
from factura.models import Factura
import logging

logger = logging.getLogger(__name__)

def desvincular_empleados_servicio(servicio):
    """
    Función auxiliar para desvincular empleados de un servicio
    """
    # Desvincular empleados de las frecuencias del servicio
    for frecuencia in servicio.frecuencias.all():
        frecuencia.empleados.clear()
    
    # Desvincular empleados directamente del servicio
    servicio.empleado.clear()
    
    logger.info(f"Empleados desvinculados del servicio ID: {servicio.id}")

def actualizar_estados_servicios():
    hoy = timezone.now().date()
    logger.info(f"Iniciando actualización de estados de servicios para fecha: {hoy}")
    
    # Iniciar servicios contratados
    servicios_a_iniciar = Servicio.objects.filter(estado=3, fecha_inicio=hoy)
    iniciados_ids = list(servicios_a_iniciar.values_list('id', flat=True))
    count_iniciados = servicios_a_iniciar.update(estado=4)
    if count_iniciados > 0:
        logger.info(f"Se iniciaron {count_iniciados} servicios (Contratado -> En Curso): {iniciados_ids}")
    
    # Finalizar servicios en curso
    servicios_a_finalizar = Servicio.objects.filter(estado=4, fecha_finaliza=hoy)
    finalizados_ids = []
    for servicio in servicios_a_finalizar:
        if not Factura.objects.filter(servicio=servicio, fechaPago__isnull=True).exists():
            servicio.estado = 6
            servicio.save()
            finalizados_ids.append(servicio.id)
            
            # Desvincular empleados del servicio finalizado
            desvincular_empleados_servicio(servicio)
    
    if finalizados_ids:
        logger.info(f"Se finalizaron {len(finalizados_ids)} servicios (En Curso -> Finalizado): {finalizados_ids}")
    
    # Marcar servicios como vencidos
    fecha_limite = hoy - timedelta(days=30)
    print("fecha_limite:", fecha_limite)
    
    servicios_con_facturas_vencidas = Servicio.objects.filter(
        Q(estado=3) | Q(estado=4),
        factura__fechaPago__isnull=True,
        factura__fecha_vencimiento__lt=fecha_limite
    ).distinct()
    
    vencidos_ids = []
    for servicio in servicios_con_facturas_vencidas:
        if Factura.objects.filter(servicio=servicio, fechaPago__isnull=True, fecha_vencimiento__lt=fecha_limite).exists():
            servicio.estado = 2
            servicio.save()
            vencidos_ids.append(servicio.id)
            
            # Desvincular empleados del servicio vencido
            desvincular_empleados_servicio(servicio)
    
    if vencidos_ids:
        logger.info(f"Se marcaron como vencidos {len(vencidos_ids)} servicios: {vencidos_ids}")
    
    logger.info("Finalizada la actualización de estados de servicios")
    return {
        'iniciados': count_iniciados,
        'finalizados': len(finalizados_ids),
        'vencidos': len(vencidos_ids)
    }

