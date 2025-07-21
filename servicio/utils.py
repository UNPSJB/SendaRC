from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from servicio.models import Servicio
from factura.models import Factura
import logging

logger = logging.getLogger(__name__)

def actualizar_estados_servicios():
    """
    Actualiza automáticamente los estados de los servicios según las reglas de negocio
    """
    hoy = timezone.now().date()
    logger.info(f"Iniciando actualización de estados de servicios para fecha: {hoy}")
    
    # 1. Cambiar servicios CONTRATADOS a EN CURSO si su fecha de inicio es hoy
    servicios_a_iniciar = Servicio.objects.filter(
        estado=3,  # Contratado
        fecha_inicio=hoy
    )
    
    count_iniciados = servicios_a_iniciar.update(estado=4)  # En Curso
    if count_iniciados > 0:
        logger.info(f"Se iniciaron {count_iniciados} servicios (Contratado -> En Curso)")
    
    # 2. Cambiar servicios EN CURSO a FINALIZADO si todas las facturas están pagas y fecha fin es hoy
    servicios_a_finalizar = Servicio.objects.filter(
        estado=4,  # En Curso
        fecha_finaliza=hoy
    )
    
    finalizados = 0
    for servicio in servicios_a_finalizar:
        # Verificar que todas las facturas del servicio estén pagadas
        facturas_impagas = Factura.objects.filter(
            servicio=servicio,
            fechaPago__isnull=True
        ).count()
        
        if facturas_impagas == 0:
            servicio.estado = 6  # Finalizado
            servicio.save()
            finalizados += 1
    
    if finalizados > 0:
        logger.info(f"Se finalizaron {finalizados} servicios (En Curso -> Finalizado)")
    
    # 3. Cambiar servicios a VENCIDO si tienen facturas impagas con más de 1 mes
    fecha_limite = hoy - timedelta(days=30)
    
    # Buscar servicios que tengan facturas vencidas por más de 30 días
    servicios_con_facturas_vencidas = Servicio.objects.filter(
        Q(estado=3) | Q(estado=4),  # Contratado o En Curso
        factura__fechaPago__isnull=True,
        factura__fecha_vencimiento__lt=fecha_limite
    ).distinct()
    
    vencidos = 0
    for servicio in servicios_con_facturas_vencidas:
        # Verificar que efectivamente tenga facturas vencidas hace más de 30 días
        facturas_muy_vencidas = Factura.objects.filter(
            servicio=servicio,
            fechaPago__isnull=True,
            fecha_vencimiento__lt=fecha_limite
        ).exists()
        
        if facturas_muy_vencidas:
            servicio.estado = 2  # Vencido
            servicio.save()
            vencidos += 1
    
    if vencidos > 0:
        logger.info(f"Se marcaron como vencidos {vencidos} servicios")
    
    logger.info("Finalizada la actualización de estados de servicios")
    return {
        'iniciados': count_iniciados,
        'finalizados': finalizados,
        'vencidos': vencidos
    }