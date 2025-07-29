#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time


def run_crons():
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SendaRC.settings')
    django.setup()

    from servicio.utils import actualizar_estados_servicios

    while True:
        print("⏱ Ejecutando actualización automática de servicios (cada 24hs)...")
        try:
            actualizar_estados_servicios()
        except Exception as e:
            print(f"❌ Error al ejecutar el cron: {e}")
        time.sleep(3600)  # Espera de 1 hora (3600 segundos)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SendaRC.settings')

    # Solo iniciar hilo del cron si estamos corriendo el servidor de desarrollo
    if 'runserver' in sys.argv:
        threading.Thread(target=run_crons, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()
