# servicio/apps.py

from django.apps import AppConfig
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)

class ServicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicio'
    
    def ready(self):
        """
        Se ejecuta cuando la aplicación está completamente cargada.
        Ideal para lanzar tareas periódicas en background.
        """
        # Importar los signals para que se registren
        import factura.signals
        
        if self.should_run_auto_update():
            # Lanzar el cron en un hilo separado
            threading.Thread(target=self.run_crons, daemon=True).start()
    
    def should_run_auto_update(self):
        """
        Determina si debe ejecutar la actualización automática.
        Evita ejecutarse durante migraciones, tests, etc.
        """
        skip_commands = [
            'migrate', 'makemigrations', 'test', 'shell', 
            'collectstatic', 'createsuperuser', 'dbshell'
        ]
        
        if (
            'runserver' in sys.argv or 
            'gunicorn' in sys.argv[0] or 
            'uwsgi' in sys.argv[0] or
            'manage.py' not in sys.argv[0]
        ):
            if not any(cmd in sys.argv for cmd in skip_commands):
                return True
        
        return False

    def run_crons(self):
        """
        Ejecuta `actualizar_estados_servicios()` cada 5 minutos (300 segundos).
        """
        from servicio.utils import actualizar_estados_servicios

        while True:
            logger.info("⏱ Ejecutando actualización automática de servicios...")
            try:
                actualizar_estados_servicios()
            except Exception as e:
                logger.error(f"❌ Error en actualización automática de servicios: {str(e)}")
            time.sleep(300)  # Esperar 5 minutos
