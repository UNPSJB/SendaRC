from django.urls import path, include
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios.as_view(), name = 'gestionServicios'),
    path('gestionServicios/<int:pk>', canvasServicio, name='canvasServicio'),
    path('presupuestarCliente/', presupuestarCliente, name = 'presupuestarCliente'),
    path('presupuestarIdCliente/<int:pk>/', presupuestarIdCliente, name = 'presupuestarIdCliente'),
    path('presupuestarServicios/', presupuestarServicios, name = 'presupuestarServicios'),
    path('presupuestarFrecuencias/', presupuestarFrecuencias, name = 'presupuestarFrecuencias'),
    path('presupuestarConfirmar/', presupuestarConfirmar, name = 'presupuestarConfirmar'),
    path('presupuestarImprimir/<int:pk>/', presupuestarImprimir, name = 'presupuestarImprimir'),
    path('presupuestarModificarImprimir/<int:pk>/', presupuestarImprimir, name = 'presupuestarModificarImprimir'),
    path('pdfImprimir/<int:pk>/', pdfImprimir, name = 'pdfImprimir'),
    path('detalleServicio/<int:pk>/', detalleServicio, name = 'detalleServicio'),
    #Modificar Presupuestos
    path('modificarPresupuesto/<int:pk>/', presupuestarCliente, name = 'modificarPresupuesto'),
    #Contratar Servicio
    path('contratarServicio/<int:pk>/', contratarServicio.as_view(), name = 'contratarServicio'),
    path('contratarServicio/<int:pk>/success', contratarServicioCorrecto, name= 'contratarServicioCorrecto'),
    path('asignarEmpleados/<int:pk>/', asignarEmpleados, name = 'asignarEmpleados'),
    path('error/', errorServicio.as_view(), name = 'errorServicio'),
    #Facturas
    path('factura/', include('factura.urls')),
    path("cancelar-servicio/<int:pk>/", cancelar_servicio, name="cancelarServicio"),
    path("eliminar-presupuesto/<int:pk>/", eliminar_presupuesto, name="eliminarPresupuesto"),
    #Reclamos
    path('registrarReclamo/', altaReclamo.as_view(), name = 'altaReclamo'),
    path('gestionReclamos/', gestionReclamos.as_view(), name = 'gestionReclamos'),
    path('api/empleados-por-servicio/<int:servicio_id>/', empleados_por_servicio, name='empleados_por_servicio'),
    #Asistencia
    path('registroAsistencia/<int:servicio_id>/', RegistrarAsistenciaView.as_view(), name = 'registroAsistencia'),
    path('gestionAsistencia/', GestionAsistencia.as_view(), name = 'gestionAsistencia'),
]
 