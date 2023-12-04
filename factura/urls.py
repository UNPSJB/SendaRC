from django.urls import path
from factura.views import *

urlpatterns = [
    
    path('', facturas, name = 'facturas'),
    path('serviciosFacturar/', serviciosFacturar, name = 'serviciosFacturar'),
    path('serviciosFacturar/<int:pk>', generarFactura, name = 'generarFactura'),
    path('facturaRegistrada/<int:pk>', facturaRegistrada, name = 'facturaRegistrada'),
    path('serviciosCobrar/', serviciosCobrar.as_view(), name = 'serviciosCobrar'),
    path('serviciosCobrar/<int:pk>', detalleServicioFactura, name='detalleServicioFactura'),
    path('facturasServicio/<int:pk>', facturasServicio, name = 'facturasServicio'),
    path('detalleFactura/<int:pk>', detalleFactura, name = 'detalleFactura'),
    path('formaPago/<int:pk>', formaPago, name = 'formaPago'),
]
