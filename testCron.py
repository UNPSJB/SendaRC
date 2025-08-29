import os
import django
import threading
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SendaRC.settings")
django.setup()

from servicio.utils import actualizar_estados_servicios

def run_crons():
    while True:
        print("⏱ Ejecutando cron...")
        actualizar_estados_servicios()
        time.sleep(10)  # ponelo en 10 seg para probar rápido

if __name__ == "__main__":
    run_crons()
