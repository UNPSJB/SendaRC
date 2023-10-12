from django.urls import path
from core.views import *

urlpatterns = [

    path('altaCliente/', altaCliente, name = 'altaCliente'),
    path('gestionClientes/', gestionClientes, name = 'gestionClientes'),
    path('altaInsumo/', altaInsumo.as_view(), name = 'altaInsumo'),
    path('gestionInsumos/', gestionInsumos.as_view(), name = 'gestionInsumos'),
    path('modificarInsumo/<int:pk>', updateInsumo.as_view(), name = 'modificarInsumo'),
    path('altaTipoServicio/(?)', altaTipoServicio, name='altaTipoServicio'),
    path('gestionTipoServicio/', gestionTipoServicio, name='gestionTipoServicio'),
]