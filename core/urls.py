from django.urls import path
from core.views import *

urlpatterns = [
    path('altaCliente/', altaCliente),
    path('gestionClientes/', gestionClientes),
    path('altaInsumo/', altaInsumo),
    path('gestionInsumo/', gestionInsumo),
    path('modificarInsumo/', modificarInsumo)
]