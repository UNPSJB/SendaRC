from django.urls import path
from core.views  import *

urlpatterns = [

    path('altaCliente/', altaCliente.as_view(), name = 'altaCliente'),
    path('gestionClientes/', gestionClientes.as_view(), name = 'gestionClientes'),
    path('modificarCliente/<int:pk>', updateCliente.as_view(), name = 'modificarCliente'),

    path('altaInsumo/', altaInsumo.as_view(), name = 'altaInsumo'),
    path('gestionInsumos/', gestionInsumos.as_view(), name = 'gestionInsumos'),
    path('modificarInsumo/<int:pk>', updateInsumo.as_view(), name = 'modificarInsumo'),

    path('altaTipoServicio/(?)', altaTipoServicio, name='altaTipoServicio'),
    path('gestionTipoServicio/', gestionTipoServicio, name='gestionTipoServicio'),
    path('altaMaquinaria/', altaMaquinaria.as_view(), name='altaMaquinaria'),
]

