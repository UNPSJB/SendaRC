from django.urls import path
from factura.views import *

urlpatterns = [
    path('', facturas, name = 'facturas'),
    path('verFacturas/', verFacturas, name='verFacturas'),
    path('facturas/ajax/', get_facturas_ajax, name='facturas_ajax'),
    path('serviciosFacturar/', serviciosFacturar, name = 'serviciosFacturar'),
    path('serviciosFacturar/<int:pk>', generarFactura, name = 'generarFactura'),
    path('facturaRegistrada/<int:pk>', facturaRegistrada, name = 'facturaRegistrada'),
    path('serviciosCobrar/', serviciosCobrar.as_view(), name = 'serviciosCobrar'),
    path('serviciosCobrar/<int:pk>', detalleServicioFactura, name='detalleServicioFactura'),
    path('facturasServicio/<int:pk>', facturasServicio, name = 'facturasServicio'),
    path('detalleFactura/<int:pk>', detalleFactura, name = 'detalleFactura'),
    path('formaPago/<int:pk>', formaPago, name = 'formaPago'),
    
    path('detallesFacturaSeña/<int:pk>', detallesFacturaSeña, name = 'detallesFacturaSeña'),
    path('generarFacturaSeña/servicio/<int:pk>', crearFacturaSeña, name = 'crearFacturaSeña'),
    path('realizarCobroFacturaSeña/<int:pk>', realizarCobroFacturaSeña, name = 'realizarCobroFacturaSeña'),
    path('facturaPagada/<int:pk>', facturaPagada, name = 'facturaPagada'),

    # Generar PDF de factura
    path("factura/<int:factura_id>/pdf/", generar_pdf_factura, name="pdf_factura"),
    
]
