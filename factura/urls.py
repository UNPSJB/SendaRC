from django.urls import path
from factura.views import *

urlpatterns = [
    
    path('detallesFacturaSeña/<int:pk>', detallesFacturaSeña, name = 'detallesFacturaSeña'),
    path('generarFacturaSeña/servicio/<int:pk>', crearFacturaSeña, name = 'crearFacturaSeña'),
    path('realizarCobroFacturaSeña/<int:pk>', realizarCobroFacturaSeña, name = 'realizarCobroFacturaSeña'),
    path('facturaPagada/<int:pk>', facturaPagada, name = 'facturaPagada'),
]