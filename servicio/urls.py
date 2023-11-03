from django.urls import path
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios, name = 'gestionServicios'),
    path('presupuestarCliente/', presupuestarCliente, name = 'presupuestarCliente'),
    path('presupuestarServicios/', presupuestarServicios, name = 'presupuestarServicios'),
    path('presupuestarFrecuencias/', presupuestarFrecuencias, name = 'presupuestarFrecuencias'),
    path('presupuestarConfirmar/', presupuestarConfirmar, name = 'presupuestarConfirmar'),
    path('presupuestarImprimir/', presupuestarImprimir, name = 'presupuestarImprimir'),
]