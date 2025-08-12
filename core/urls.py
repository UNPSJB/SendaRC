from django.urls import path
from .views import *

urlpatterns = [

    path('altaSancion/', altaSancion.as_view(), name = 'altaSancion'),
    path('gestionSanciones/', gestionSancion.as_view(), name = 'gestionSanciones'),
    path('gestionSanciones/<int:pk>', detalleSancion, name='detalleSancion'),

    path('altaEmpleado/', altaEmpleado.as_view(), name = 'altaEmpleado'),
    path('modificarEmpleado/<int:pk>', updateEmpleado.as_view(), name = 'modificarEmpleado'),
    path('gestionEmpleado/', gestionEmpleado.as_view(), name = 'gestionEmpleado'),
    path('gestionEmpleado/<int:pk>', detalleEmpleado, name='detalleEmpleado'),
    
    path('altaLocalidad/', altaLocalidad.as_view(), name = 'altaLocalidad'),
    path('modificarLocalidad/<int:pk>', updateLocalidad.as_view(), name = 'modificarLocalidad'),
    path('gestionLocalidad/', gestionLocalidad.as_view(), name = 'gestionLocalidad'),

    path('altaCliente/', altaCliente.as_view(), name = 'altaCliente'),
    path('gestionClientes/', gestionClientes.as_view(), name = 'gestionClientes'),
    path('modificarCliente/<int:pk>', updateCliente.as_view(), name = 'modificarCliente'),
    path('gestionClientes/<int:pk>', detalleCliente, name='detalleCliente'),

    path('altaInsumo/', altaInsumo.as_view(), name = 'altaInsumo'),
    path('gestionInsumos/', gestionInsumos.as_view(), name = 'gestionInsumos'),
    path('modificarInsumo/<int:pk>', updateInsumo.as_view(), name = 'modificarInsumo'),

    path('altaTipoServicio/', altaTipoServicio.as_view(), name='altaTipoServicio'),
    path('gestionTipoServicio/', gestionTipoServicio.as_view(), name='gestionTipoServicio'),
    path('modificarTipoServicio/<int:pk>', updateTipoServicio.as_view(), name='modificarTipoServicio'),
    path('gestionTipoServicio/<int:pk>', tipoServicioDetalles, name='detalleTipoServicio'),
    path('tipo-servicio/<int:pk>/editar-insumos/', editar_cant_insumos_servicio, name="editarCantInsumosServicio"),
    
    path('altaMaquinaria/', altaMaquinaria.as_view(), name='altaMaquinaria'), 
    path('modificarMaquinaria/<int:pk>', updateMaquinaria.as_view(), name='modificarMaquinaria'),
    path('gestionMaquinaria/', gestionMaquinaria.as_view(), name='gestionMaquinaria'),
    path('gestionMaquinaria/<int:pk>', maquinariaDetalles, name='detalleMaquinaria'),

    path('calendario/', calendario, name='calendario'),
    path('calendario/eventos/', eventos_calendario, name='eventos_calendario'),
]