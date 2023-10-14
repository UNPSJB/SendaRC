from django.urls import path
from servicio.views import *

urlpatterns = [
    path('gestionServicios/', gestionServicios, name = 'gestionServicios'),
]