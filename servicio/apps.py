# servicio/apps.py

from django.apps import AppConfig
import logging
import sys

logger = logging.getLogger(__name__)

class ServicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicio'
    
    def ready(self):
        """
        Se ejecuta cuando la aplicación está completamente cargada
        """
        # Importar los signals para que se registren
        import factura.signals  # Esto registra todos los signals
        
        # Solo ejecutar la actualización inicial en el servidor principal
        if self.should_run_auto_update():
            try:
                logger.info("Ejecutando actualización automática de estados de servicios...")
                from servicio.utils import actualizar_estados_servicios
                actualizar_estados_servicios()
            except Exception as e:
                logger.error(f"Error en actualización automática de servicios: {str(e)}")
    
    def should_run_auto_update(self):
        """
        Determina si debe ejecutar la actualización automática
        """
        # Comandos donde NO queremos ejecutar la actualización
        skip_commands = [
            'migrate', 'makemigrations', 'test', 'shell', 
            'collectstatic', 'createsuperuser', 'dbshell'
        ]
        
        # Solo ejecutar si estamos corriendo el servidor
        if (
            'runserver' in sys.argv or 
            'gunicorn' in sys.argv[0] or 
            'uwsgi' in sys.argv[0] or
            'manage.py' not in sys.argv[0]  # Para servidores en producción
        ):
            # Verificar que no sea un comando que debemos evitar
            if not any(cmd in sys.argv for cmd in skip_commands):
                return True
        
        return False