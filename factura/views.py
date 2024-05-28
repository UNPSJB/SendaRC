from django.shortcuts import render, redirect
from servicio.models import *
from core.models import *
from .models import *
from .forms import *
from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

#10 Dias antes de finde mes y vence 10 Dias despues que comienza el mes siguiente
@login_required
def facturas(request):
    return render(request, 'factura/facturas.html')

@login_required
def serviciosFacturar(request):
    fecha_actual = timezone.now().date()
    ultimo_dia_mes = timezone.now().date() + timedelta(days=(32 - timezone.now().date().day))
    fecha_limite = ultimo_dia_mes - timedelta(days=10)
    servicios = []

    if request.method == 'GET': 
        if len(request.GET) > 0: 
            form = SelectClienteForm(request.GET)
            cliente = Cliente.habilitados.get(pk=request.GET.get('cliente', ''))
            
            # Logica para servicios contratados y eventuales, ya son los unicos que se van a poder generar facturas cuando estan contratados
            servicios_contratados = Servicio.objects.filter(estado=3, cliente=cliente)
            for servicio in servicios_contratados:
                # Eventuales facturar antes de iniciar el servicio,  
                if servicio.tipo == 1 and fecha_actual < servicio.fecha_inicio:
                    if cliente.tipo == 1 and len(Factura.objects.filter(servicio=servicio)) < 2:
                        servicios.append(servicio)
                    elif cliente.tipo == 2 and len(Factura.objects.filter(servicio=servicio)) < 1:
                        servicios.append(servicio)
            
            # Logica para servicios en curso y determinados, ya son los unicos que se van a poder generar facturas cuando estan en curso
            if fecha_actual <= ultimo_dia_mes and fecha_actual >= fecha_limite:    
                # Logica para servicios en curso y determinados, ya que son los unicos que se van a poder generar factura si estan en curso
                servicios_en_curso = Servicio.objects.filter(estado=4, cliente=cliente)
                for servicio in servicios_en_curso:
                    # Determinados facturar los ultimos dias del mes en el que se realizo el servicio
                    if servicio.tipo == 2 and fecha_actual >= servicio.fecha_inicio and fecha_actual <= servicio.fecha_finaliza:
                        servicio_facturas = Factura.objects.filter(servicio=servicio)
                        for factura in servicio_facturas:
                            if factura.periodoServicio != fecha_actual.month or factura.tipo == 1:
                                servicios.append(servicio)
        else:
            form = SelectClienteForm()    
                    
    return render(request, 'factura/serviciosFacturar.html', {'form': form, 'servicios': servicios})

@login_required
def generarFactura(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    fecha_actual = timezone.now().date()
    print("-------------EN GENERAR FACTURA, MES:", fecha_actual.month)
    if fecha_actual.month == 12:  
        primer_dia_next_mes = fecha_actual.replace(day=1, month=1)
    else:
        primer_dia_next_mes = fecha_actual.replace(day=1, month=fecha_actual.month + 1)
    
    #Fecha emision no asignamos nada por su atributo que pusimos en el model Frecuencia
    factura = Factura(fecha_vencimiento=primer_dia_next_mes.replace(day=10), 
                      cliente=servicio.cliente, servicio=servicio)
    
    # Logica cuando es servicio eventual y cliente ocasional o habitual 
    if servicio.tipo == 1 and servicio.cliente.tipo == 1:
        factura.importe = servicio.importe_total * 0.5 # calculo para el 50%
        factura.tipo = 2
        factura.periodoServicio = 13
    elif servicio.tipo == 1 and servicio.cliente.tipo == 2: 
        factura.importe = servicio.importe_total
        factura.tipo = 2
        factura.periodoServicio = 13
    # Logica cuando es servicio determinado y cliente ocasional o habitual 
    elif servicio.tipo == 2 and servicio.cliente.tipo == 1:
        factura_seña = Factura.objects.get(servicio=servicio, tipo=1)
        if Factura.objects.get(servicio=servicio, tipo=3, importe=factura_seña.importe):
            factura.importe = servicio.importe_total
            factura.tipo = 3
        else:
            factura.importe = servicio.importe_total * 0.5 # calculo para el 50%
            factura.tipo = 3
        factura.periodoServicio = fecha_actual.month
    elif servicio.tipo == 2 and servicio.cliente.tipo == 2: 
        factura.importe = servicio.importe_total
        factura.tipo = 3
        factura.periodoServicio = fecha_actual.month
    
    factura.save()
    
    servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(servicio=servicio)
    for tipo in servicio_tipos_servicios:
        tipo_servicio = TipoServicio.habilitados.get(pk=tipo.tipoServicio.pk)
        Detalle_Servicios.objects.create(factura=factura, tipo_servicio=tipo_servicio.descripcion, tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
                                         precio_tipo_servicio=tipo_servicio.precio, cantidad=tipo.cantidad)
    
    if servicio.tipo == 'Determinado':
        cant_empleados = len(Frecuencia.objects.filter(servicio=servicio)) * servicio.cant_empleados *  4
    else:
        cant_empleados = len(Frecuencia.objects.filter(servicio=servicio)) * servicio.cant_empleados    
    mano_obra =  Empleado.getSueldoBasico() / 24     
    Detalle_Empleados.objects.create(factura=factura, cantidad_empleados=servicio.cant_empleados, importe_mano_obra=(mano_obra * cant_empleados))
    
    return redirect('facturaRegistrada', factura.pk)

@login_required
def facturaRegistrada(request, pk):
    factura = Factura.objects.get(pk=pk)
    return render(request, 'factura/facturaRegistrada.html', {'factura': factura})

@method_decorator(login_required, name='dispatch')   
class serviciosCobrar(ListView):
    model = Servicio
    template_name = 'factura/serviciosCobrar.html'
    context_object_name = 'servicios'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context['form'] = SelectClienteForm(self.request.GET)
        else:
            context['form'] = SelectClienteForm()
        return context
    
    def get_queryset(self):
        queryset = Servicio.objects.filter(estado__in=[3, 4, 5])
        cliente = self.request.GET.get('cliente', '')
        if cliente: 
            queryset = queryset.filter(cliente=cliente)                      
        else:
            queryset = None
        return queryset

@login_required
def detalleServicioFactura(request, pk):
    servicio = Servicio.objects.get(id=pk)
    return render(request, 'factura/detalleServicioFactura.html', {'servicio': servicio})

@login_required
def facturasServicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    facturas = Factura.objects.filter(servicio=servicio)
    
    return render(request, 'factura/facturasServicio.html', {'facturas': facturas})

@login_required
def detalleFactura(request, pk):
    factura = Factura.objects.get(pk=pk)
    detalles_servicios = []
    detalle_empleado = []
    if factura.tipo != 1:
        detalles_servicios = Detalle_Servicios.objects.filter(factura=factura)
        detalle_empleado = Detalle_Empleados.objects.get(factura=factura)

    return render(request, 'factura/detalleFactura.html', {'factura': factura, 'detalles_servicios': detalles_servicios, 'detalle_empleado': detalle_empleado})

@login_required
def formaPago(request, pk):
    factura = Factura.objects.get(pk=pk)
    form = FormaPagoForm()
    
    if (request.method == 'POST'):
        form = FormaPagoForm(request.POST)
        if form.is_valid():
            tipo_pago = form.cleaned_data['forma']
            factura.fechaPago = timezone.now().date()
            if tipo_pago == 'Efectivo':
                factura.formaPago = 1
            else:
                factura.formaPago = 3
            
            factura.save()
            return redirect('facturasServicio', factura.servicio.pk)
        else:
            print(form.errors)
    else:
        print(factura)
        
    return render(request, 'factura/formaPago.html', {'form': form, 'factura': factura, 'servicio': factura.servicio})

@login_required
def crearFacturaSeña(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    cliente = servicio.cliente
    factura_seña = Factura.objects.create(servicio=servicio, 
        importe=servicio.importe_total*0.50, 
        cliente=cliente,
        tipo=1,
        fechaEmision=datetime.now())
    factura_seña.save()
    return redirect(to='detallesFacturaSeña', pk=factura_seña.pk)

@login_required
def detallesFacturaSeña(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    return render(request, 'factura/detallesFacturaSeña.html', {'factura_seña':factura_seña})

@login_required
def realizarCobroFacturaSeña(request, pk):
    if request.method == 'POST':
        factura_seña = Factura.objects.get(pk=pk)
        form = FormCobroFacturaSeña(request.POST)
        if form.is_valid():
            factura_seña.formaPago = form.cleaned_data['formapago']
            factura_seña.fechaPago = datetime.now()
            factura_seña.save()            
            servicio = Servicio.objects.get(pk=factura_seña.servicio.pk)
            servicio.estado = 3
            servicio.save()
            return redirect('facturaPagada', pk=factura_seña.pk)
        else:
            print(form.errors)
        return render(request, '')
    facturaSeña = Factura.objects.get(pk=pk)
    servicio = facturaSeña.servicio
    form = FormCobroFacturaSeña()
    context = {
        'servicio': servicio,
        'facturaSeña':facturaSeña,
        'form': form
    }
    return render(request, 'factura/CobroFacturaSeña.html', context)

@login_required
def facturaPagada(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    context = {
        'factura_seña':factura_seña
    }
    return render(request, 'factura/facturaSeñaPagada.html', context)
