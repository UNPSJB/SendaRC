from django.urls import path
from core.views import *

urlpatterns = [
    path('altaInsumo/', altaInsumo),
    path('altaCliente/', altaCliente),
    path('gestionClientes/', gestionClientes),
    path('altaTipoServicio/', altaTipoServicio)
]