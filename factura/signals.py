# factura/signals.py 

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from factura.models import Factura
from servicio.models import Servicio
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Factura)
def verificar_pago_completo_servicio(sender, instance, created, **kwargs):
    """
    Se ejecuta cada vez que se guarda una factura.
    Verifica si todas las facturas del servicio están pagadas para cambiar estado.
    """
    # Solo procesar si la factura fue pagada (tiene fechaPago)
    if instance.fechaPago:
        servicio = instance.servicio
        logger.info(f"Factura {instance.id} del servicio {servicio.id} fue pagada. Verificando estado del servicio...")
        
        # Verificar si todas las facturas del servicio están pagadas
        facturas_impagas = Factura.objects.filter(
            servicio=servicio,
            fechaPago__isnull=True
        ).count()
        
        if facturas_impagas == 0:
            # Todas las facturas están pagadas
            hoy = timezone.now().date()
            
            # Si el servicio está vencido y se pagaron todas las facturas
            if servicio.estado == 2:  # Vencido
                if servicio.fecha_inicio and servicio.fecha_inicio <= hoy:
                    if servicio.fecha_finaliza and servicio.fecha_finaliza <= hoy:
                        # Ya terminó, pasar a finalizado
                        servicio.estado = 6  # Finalizado
                        logger.info(f"Servicio {servicio.id} cambió de Vencido a Finalizado (todas facturas pagadas)")
                    else:
                        # Aún no terminó, pasar a en curso
                        servicio.estado = 4  # En Curso
                        logger.info(f"Servicio {servicio.id} cambió de Vencido a En Curso (todas facturas pagadas)")
                else:
                    # Aún no empezó, pasar a contratado
                    servicio.estado = 3  # Contratado
                    logger.info(f"Servicio {servicio.id} cambió de Vencido a Contratado (todas facturas pagadas)")
                
                servicio.save()
            
            # Si el servicio está en curso y llegó a su fecha fin
            elif servicio.estado == 4 and servicio.fecha_finaliza and servicio.fecha_finaliza <= hoy:
                servicio.estado = 6  # Finalizado
                servicio.save()
                logger.info(f"Servicio {servicio.id} cambió de En Curso a Finalizado (todas facturas pagadas y fecha fin alcanzada)")

@receiver(pre_save, sender=Factura)
def detectar_cambio_pago_factura(sender, instance, **kwargs):
    """
    Detecta cuando una factura cambia de impaga a pagada
    """
    if instance.pk:  # Solo si la factura ya existe
        try:
            factura_anterior = Factura.objects.get(pk=instance.pk)
            # Si antes no tenía fechaPago y ahora sí
            if not factura_anterior.fechaPago and instance.fechaPago:
                logger.info(f"Detectado pago de factura {instance.id} del servicio {instance.servicio.id}")
        except Factura.DoesNotExist:
            pass

# Función auxiliar para verificar estado después del pago
def actualizar_estado_por_pago(servicio):
    """
    Lógica para determinar el nuevo estado del servicio cuando se pagan todas las facturas
    """
    hoy = timezone.now().date()
    
    # Si el servicio ya finalizó por fecha
    if servicio.fecha_finaliza and servicio.fecha_finaliza <= hoy:
        return 6  # Finalizado
    
    # Si el servicio ya empezó
    elif servicio.fecha_inicio and servicio.fecha_inicio <= hoy:
        return 4  # En Curso
    
    # Si el servicio aún no empezó
    else:
        return 3  # Contratado

# Signal adicional para monitorear cambios en el estado de servicio
@receiver(post_save, sender=Servicio)
def log_cambio_estado_servicio(sender, instance, created, **kwargs):
    """
    Registra en el log cuando cambia el estado de un servicio
    """
    if not created:  # Solo si no es un servicio nuevo
        try:
            # Obtener el estado anterior si existe
            if hasattr(instance, '_old_estado'):
                estado_anterior = instance._old_estado
                estado_actual = instance.estado
                
                if estado_anterior != estado_actual:
                    logger.info(f"Servicio {instance.id} cambió de estado: {instance.getEstado()} (código {estado_actual})")
        except:
            pass

@receiver(pre_save, sender=Servicio)
def guardar_estado_anterior(sender, instance, **kwargs):
    """
    Guarda el estado anterior para poder detectar cambios
    """
    if instance.pk:
        try:
            servicio_anterior = Servicio.objects.get(pk=instance.pk)
            instance._old_estado = servicio_anterior.estado
        except Servicio.DoesNotExist:
            pass