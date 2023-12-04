from django.urls import path
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios.as_view(), name = 'gestionServicios'),
    path('gestionServicios/<int:pk>', detalleServicio, name='detalleServicio'),
    path('presupuestarCliente/', presupuestarCliente, name = 'presupuestarCliente'),
    path('presupuestarIdCliente/<int:pk>/', presupuestarIdCliente, name = 'presupuestarIdCliente'),
    path('presupuestarServicios/', presupuestarServicios, name = 'presupuestarServicios'),
    path('presupuestarFrecuencias/', presupuestarFrecuencias, name = 'presupuestarFrecuencias'),
    path('presupuestarConfirmar/', presupuestarConfirmar, name = 'presupuestarConfirmar'),
    path('presupuestarImprimir/<int:pk>/', presupuestarImprimir, name = 'presupuestarImprimir'),
    path('presupuestarModificarImprimir/<int:pk>/', presupuestarImprimir, name = 'presupuestarModificarImprimir'),
    path('pdfImprimir/<int:pk>/', pdfImprimir, name = 'pdfImprimir'),
    path('detallePresupuesto/<int:pk>/', detallePresupuesto, name = 'detallePresupuesto'),
    #Modificar Presupuestos
    path('modificarPresupuesto/<int:pk>/', presupuestarCliente, name = 'modificarPresupuesto'),
    #Contratar Servicio
    path('contratarServicio/<int:pk>/', contratarServicio.as_view(), name = 'contratarServicio'),
    path('contratarServicio/<int:pk>/success', contratarServicioCorrecto, name= 'contratarServicioCorrecto'),
    path('asignarEmpleados/<int:pk>/', asignarEmpleados, name = 'asignarEmpleados'),
    path('error/', errorServicio.as_view(), name = 'errorServicio'),
]
 