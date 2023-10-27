from django.urls import path
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios, name = 'gestionServicios'),
    path('presupuestar1/', presupuestarCliente, name = 'presupuestarCliente'),
    path('presupuestar2/', presupuestarServicios, name = 'presupuestarServicios'),
    path('presupuestar3/', presupuestarConfirmar, name = 'presupuestarConfirmar'),
    path('presupuestar4/', presupuestarImprimir, name = 'presupuestarImprimir'),
]