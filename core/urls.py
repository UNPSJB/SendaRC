from django.urls import path
from core.views import *

urlpatterns = [

    path('altaCliente/', altaCliente, name = 'altaCliente'),
    path('gestionClientes/', gestionClientes, name = 'gestionClientes'),
    path('altaInsumo/', altaInsumo, name = 'altaInsumo'),
    path('gestionInsumos/', gestionInsumos, name = 'gestionInsumos'),
    path('modificarInsumo/', modificarInsumo, name = 'modificarInsumo'),
    path('altaTipoServicio/', altaTipoServicio)
]