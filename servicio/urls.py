from django.urls import path
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios.as_view(), name = 'gestionServicios'),
    path('presupuestarCliente/', presupuestarCliente, name = 'presupuestarCliente'),
    path('presupuestarServicios/', presupuestarServicios, name = 'presupuestarServicios'),
    path('presupuestarFrecuencias/', presupuestarFrecuencias, name = 'presupuestarFrecuencias'),
    path('presupuestarConfirmar/', presupuestarConfirmar, name = 'presupuestarConfirmar'),
    path('presupuestarImprimir/', presupuestarImprimir, name = 'presupuestarImprimir'),
    #Modificar Presupuestos
    path('modificarPresupuesto/<int:pk>/', presupuestarCliente, name = 'modificarPresupuesto'),
]