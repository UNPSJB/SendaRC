from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from servicio.models import Servicio
from factura.models import Factura
import logging
from django.utils.timezone import get_current_timezone, is_naive, make_aware


logger = logging.getLogger(__name__)

def get_primer_horario_inicio(servicio):
    """
    Devuelve un datetime aware con la hora de inicio del turno más temprano en la fecha de inicio del servicio.
    """
    if not servicio.fecha_inicio:
        logger.warning(f"Servicio {servicio.id} no tiene fecha_inicio.")
        return None

    frecuencia_min_turno = servicio.frecuencias.order_by('turno').first()
    if not frecuencia_min_turno:
        logger.warning(f"Servicio {servicio.id} no tiene frecuencias asignadas.")
        return None

    # Obtener hora de inicio del turno más temprano
    hora_inicio = frecuencia_min_turno.getHoraInicio().time()
    dt_inicio = datetime.combine(servicio.fecha_inicio, hora_inicio)

    if is_naive(dt_inicio):
        dt_inicio = make_aware(dt_inicio, get_current_timezone())

    logger.debug(f"[Servicio {servicio.id}] Hora de inicio calculada: {dt_inicio.isoformat()}")
    return dt_inicio


def get_ultimo_horario_finalizacion(servicio):
    """
    Devuelve un datetime aware en la zona horaria local del servidor (Render).
    Es la fecha final más la hora fin del último turno del servicio.
    """
    if not servicio.fecha_finaliza:
        logger.warning(f"Servicio {servicio.id} no tiene fecha_finaliza.")
        return None

    frecuencia_max_turno = servicio.frecuencias.order_by('-turno').first()
    if not frecuencia_max_turno:
        logger.warning(f"Servicio {servicio.id} no tiene frecuencias asignadas.")
        return None

    # Obtener la hora fin del turno más alto
    hora_fin = frecuencia_max_turno.getHoraFin().time()

    # Combinar con la fecha final
    dt_final = datetime.combine(servicio.fecha_finaliza, hora_fin)

    # Asegurar que sea aware en la zona horaria local
    if is_naive(dt_final):
        dt_final = make_aware(dt_final, get_current_timezone())

    logger.debug(f"[Servicio {servicio.id}] Hora fin calculada: {dt_final.isoformat()}")
    return dt_final



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
    servicios_a_iniciar = Servicio.objects.filter(estado=3)
    iniciados_ids = []
    
    for servicio in servicios_a_iniciar:
        hora_inicio = get_primer_horario_inicio(servicio)
        
        if hora_inicio and timezone.now() >= hora_inicio:
            servicio.estado = 4
            servicio.save()
            iniciados_ids.append(servicio.id)

    if iniciados_ids:
        logger.info(f"Se iniciaron {len(iniciados_ids)} servicios (Contratado -> En Curso): {iniciados_ids}")
    
    # Finalizar servicios en curso
    servicios_a_finalizar = Servicio.objects.filter(estado=4)
    finalizados_ids = []

    for servicio in servicios_a_finalizar:
        hora_fin = get_ultimo_horario_finalizacion(servicio)
        
        if hora_fin and timezone.now() >= hora_fin:
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
        'iniciados': len(iniciados_ids),
        'finalizados': len(finalizados_ids),
        'vencidos': len(vencidos_ids)
    }

