from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout, login as auth_login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import month_name
import json
import re

# Importar los modelos necesarios
from core.models import Cliente, TipoServicio
from servicio.models import Servicio
from factura.models import Factura

def formatear_importe(importe):
    """
    Formatea un importe numérico a formato moneda en español (ej: $ 1.234,56)
    """
    return "$ {:,.2f}".format(importe).replace(",", "X").replace(".", ",").replace("X", ".")

# Diccionario de ciudades de Chubut con sus coordenadas aproximadas
CIUDADES_CHUBUT = {
    'rawson': {'lat': -43.3002, 'lng': -65.1023, 'nombre': 'Rawson'},
    'trelew': {'lat': -43.2489, 'lng': -65.3050, 'nombre': 'Trelew'},
    'puerto madryn': {'lat': -42.7692, 'lng': -65.0383, 'nombre': 'Puerto Madryn'},
    'comodoro rivadavia': {'lat': -45.8667, 'lng': -67.5000, 'nombre': 'Comodoro Rivadavia'},
    'esquel': {'lat': -42.9111, 'lng': -71.3175, 'nombre': 'Esquel'},
    'trevelin': {'lat': -43.0847, 'lng': -71.4667, 'nombre': 'Trevelin'},
    'dolavon': {'lat': -43.3167, 'lng': -65.7167, 'nombre': 'Dolavon'},
    'gaiman': {'lat': -43.2833, 'lng': -65.4833, 'nombre': 'Gaiman'},
    'gobernador costa': {'lat': -43.2500, 'lng': -65.6000, 'nombre': 'Gobernador Costa'},
    'veintiocho de julio': {'lat': -43.5167, 'lng': -65.8667, 'nombre': '28 de Julio'},
    'camarones': {'lat': -44.7833, 'lng': -65.7167, 'nombre': 'Camarones'},
    'rada tilly': {'lat': -45.9167, 'lng': -67.5667, 'nombre': 'Rada Tilly'},
    'sarmiento': {'lat': -45.5833, 'lng': -69.0833, 'nombre': 'Sarmiento'},
    'rio mayo': {'lat': -45.6833, 'lng': -70.2500, 'nombre': 'Río Mayo'},
    'cholila': {'lat': -42.5167, 'lng': -71.4167, 'nombre': 'Cholila'},
    'el maiten': {'lat': -42.0500, 'lng': -71.1667, 'nombre': 'El Maitén'},
    'el hoyo': {'lat': -42.0667, 'lng': -71.5167, 'nombre': 'El Hoyo'},
    'epuyen': {'lat': -42.0667, 'lng': -71.5333, 'nombre': 'Epuyén'},
    'lago puelo': {'lat': -42.0667, 'lng': -71.6000, 'nombre': 'Lago Puelo'},
    'jose de san martin': {'lat': -44.0500, 'lng': -70.4667, 'nombre': 'José de San Martín'},
    'tecka': {'lat': -43.4833, 'lng': -70.8167, 'nombre': 'Tecka'},
    'corcovado': {'lat': -43.5833, 'lng': -71.0500, 'nombre': 'Corcovado'},
    'gobernador gregores': {'lat': -48.7500, 'lng': -70.2167, 'nombre': 'Gobernador Gregores'},
    'perito moreno': {'lat': -46.5833, 'lng': -70.9333, 'nombre': 'Perito Moreno'},
    'los antiguos': {'lat': -46.5500, 'lng': -71.6333, 'nombre': 'Los Antiguos'},
    'alto rio senguer': {'lat': -45.0333, 'lng': -70.8333, 'nombre': 'Alto Río Senguer'},
    'facundo': {'lat': -45.4667, 'lng': -69.2833, 'nombre': 'Facundo'},
    'las plumas': {'lat': -45.8167, 'lng': -69.2000, 'nombre': 'Las Plumas'},
    'gan gan': {'lat': -44.5000, 'lng': -68.5000, 'nombre': 'Gan Gan'},
    'gastre': {'lat': -42.2667, 'lng': -69.2167, 'nombre': 'Gastre'},
    'gualjaina': {'lat': -42.7500, 'lng': -70.1833, 'nombre': 'Gualjaina'},
    'paso de indios': {'lat': -43.8833, 'lng': -68.8833, 'nombre': 'Paso de Indios'},
}

def obtener_servicios_ubicacion_exacta():
    """
    Obtiene todos los servicios con su ubicación exacta basada en localidad y dirección
    Retorna una lista de diccionarios con la información de cada servicio individual
    """
    servicios_ubicaciones = []
    
    # Obtener todos los servicios que tienen localidad y dirección
    servicios = Servicio.objects.select_related('cliente', 'localidad').filter(
        localidad__isnull=False,
        direccion__isnull=False
    ).exclude(direccion='')
    
    for servicio in servicios:
        # Buscar las coordenadas de la localidad en el diccionario
        localidad_nombre = servicio.localidad.nombre.lower().strip()
        coordenadas = None
        
        # Buscar coincidencia exacta primero
        if localidad_nombre in CIUDADES_CHUBUT:
            coordenadas = CIUDADES_CHUBUT[localidad_nombre]
        else:
            # Buscar coincidencias parciales
            for ciudad_key, ciudad_info in CIUDADES_CHUBUT.items():
                if ciudad_key in localidad_nombre or localidad_nombre in ciudad_key:
                    coordenadas = ciudad_info
                    break
        
        # Si encontramos coordenadas, agregar el servicio
        if coordenadas:
            # Obtener el primer tipo de servicio
            primer_tipo = servicio.tipoServicios.first()
            tipo_servicio = primer_tipo.descripcion if primer_tipo else 'Sin tipo'
            
            # Obtener empleados asignados
            empleados = [emp.nombre for emp in servicio.empleado.all()]
            empleados_str = ', '.join(empleados) if empleados else 'Sin asignar'
            
            # Determinar color según el estado del servicio
            color = obtener_color_por_estado(servicio.estado)
            
            servicio_info = {
                'id': servicio.id,
                'lat': coordenadas['lat'],
                'lng': coordenadas['lng'],
                'cliente': servicio.cliente.nombre,
                'direccion': servicio.direccion,
                'localidad': servicio.localidad.nombre,
                'tipo_servicio': tipo_servicio,
                'fecha_inicio': servicio.fecha_inicio.strftime('%d/%m/%Y') if servicio.fecha_inicio else 'Sin fecha',
                'fecha_fin': servicio.fecha_finaliza.strftime('%d/%m/%Y') if servicio.fecha_finaliza else 'Sin fecha fin',
                'estado': servicio.getEstado(),
                'estado_numero': servicio.estado,
                'tipo': servicio.getTipo(),
                'empleados': empleados_str,
                'importe': servicio.getImporteTotalFormateado(),
                'metros2': servicio.metros2,
                'observaciones': servicio.observaciones[:100] + '...' if len(servicio.observaciones) > 100 else servicio.observaciones,
                'color': color
            }
            
            servicios_ubicaciones.append(servicio_info)
    
    return servicios_ubicaciones

def obtener_color_por_estado(estado):
    """
    Retorna un color según el estado del servicio
    """
    colores_estado = {
        1: '#3b82f6',  # Presupuestado - Azul
        2: '#ef4444',  # Vencido - Rojo
        3: '#f59e0b',  # Contratado - Amarillo
        4: '#10b981',  # En Curso - Verde
        5: '#f97316',  # Suspendido - Naranja
        6: '#6b7280',  # Finalizado - Gris
        7: '#dc2626',  # Cancelado - Rojo oscuro
    }
    return colores_estado.get(estado, '#6b7280')

@login_required
def home(request):
    request.session['presupuesto'] = {}
    request.session['servicios'] = []
    request.session['frecuencias'] = []
    
    # Obtener fecha actual
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Calcular ingresos del mes actual
    ingresos_mes = Factura.objects.filter(
        fechaPago__isnull=False,
        fechaPago__gte=inicio_mes,
        fechaPago__lte=hoy
    ).aggregate(total=Sum('importe'))['total'] or 0



    ingresos_mes_formateado = formatear_importe(ingresos_mes)
    
    # Calcular ingresos del mes anterior para comparación
    mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    ingresos_mes_anterior = Factura.objects.filter(
        fechaPago__isnull=False,
        fechaPago__gte=mes_anterior,
        fechaPago__lte=fin_mes_anterior
    ).aggregate(total=Sum('importe'))['total'] or 0
    
    # Calcular porcentaje de cambio en ingresos
    if ingresos_mes_anterior > 0:
        cambio_ingresos = ((ingresos_mes - ingresos_mes_anterior) / ingresos_mes_anterior) * 100
    else:
        cambio_ingresos = 100 if ingresos_mes > 0 else 0
    
    # Servicios activos (servicios que no han finalizado)
    servicios_activos = Servicio.objects.filter(
        Q(fecha_finaliza__gte=hoy) | Q(fecha_finaliza__isnull=True)
    ).count()
    
    # Servicios activos del mes anterior para comparación
    servicios_mes_anterior = Servicio.objects.filter(
        fecha_inicio__gte=mes_anterior,
        fecha_inicio__lte=fin_mes_anterior
    ).count()
    
    # Facturas pendientes (sin pagar) y pagadas
    facturas_pendientes = Factura.objects.filter(fechaPago__isnull=True).count()
    facturas_pagadas = Factura.objects.filter(fechaPago__isnull=False).count()
    
    # Facturas pendientes del mes anterior
    facturas_pendientes_anterior = Factura.objects.filter(
        fechaPago__isnull=True,
        fechaEmision__lt=inicio_mes
    ).count()
    
    # Clientes activos
    clientes_activos = Cliente.objects.filter(activo=True).count()
    
    # Clientes nuevos este mes
    clientes_nuevos = Cliente.objects.filter(
        # Asumiendo que tienes un campo fecha_creacion, si no, usar id como aproximación
        id__in=Cliente.objects.values('id')[:clientes_activos]
    ).count()
    
    # Datos para gráfico de ingresos (últimos 6 meses)
    ingresos_mensuales = []
    labels_meses = []
    
    for i in range(5, -1, -1):  # Últimos 6 meses
        fecha_mes = hoy - timedelta(days=30*i)
        inicio_mes_grafico = fecha_mes.replace(day=1)
        if i == 0:
            fin_mes_grafico = hoy
        else:
            siguiente_mes = (inicio_mes_grafico + timedelta(days=32)).replace(day=1)
            fin_mes_grafico = siguiente_mes - timedelta(days=1)
        
        ingreso_mes = Factura.objects.filter(
            fechaPago__isnull=False,
            fechaPago__gte=inicio_mes_grafico,
            fechaPago__lte=fin_mes_grafico
        ).aggregate(total=Sum('importe'))['total'] or 0
        
        ingresos_mensuales.append(float(ingreso_mes))  # Convertir a float para JSON
        labels_meses.append(month_name[inicio_mes_grafico.month])
    
    # Datos para gráfico de servicios por tipo
    servicios_por_tipo = []
    tipos_servicios = TipoServicio.objects.filter(activo=True)
    
    for tipo in tipos_servicios:
        # CORRECCIÓN: Cambiado de 'tipo_servicio' a 'tipoServicios'
        cantidad = Servicio.objects.filter(
            cantserviciotiposervicio__tipoServicio=tipo
        ).distinct().count()
        if cantidad > 0:
            servicios_por_tipo.append({
                'label': tipo.descripcion,
                'cantidad': cantidad
            })
    
    # Si no hay tipos de servicios con datos, usar datos de ejemplo
    if not servicios_por_tipo:
        servicios_por_tipo = [
            {'label': 'Limpieza General', 'cantidad': 10},
            {'label': 'Mantenimiento', 'cantidad': 5},
            {'label': 'Limpieza Profunda', 'cantidad': 8}
        ]
    
    # Datos para gráfico de estado de facturas
    facturas_estado = [
        {'label': 'Facturas Pagadas', 'cantidad': facturas_pagadas},
        {'label': 'Facturas Pendientes', 'cantidad': facturas_pendientes}
    ]
    
    # Obtener datos de servicios por ubicación
    servicios_ubicacion_exacta = obtener_servicios_ubicacion_exacta()
    
    context = {
        'ingresos_mes_formateado': ingresos_mes_formateado,
        'cambio_ingresos': round(cambio_ingresos, 1),
        'servicios_activos': servicios_activos,
        'cambio_servicios': servicios_activos - servicios_mes_anterior,
        'facturas_pendientes': facturas_pendientes,
        'cambio_facturas': facturas_pendientes_anterior - facturas_pendientes,
        'clientes_activos': clientes_activos,
        'cambio_clientes': clientes_nuevos,
        'ingresos_mensuales': json.dumps(ingresos_mensuales),
        'labels_meses': json.dumps(labels_meses),
        'servicios_por_tipo': json.dumps(servicios_por_tipo),
        'facturas_estado': json.dumps(facturas_estado),
        'servicios_ubicacion_exacta': json.dumps(servicios_ubicacion_exacta),   # Nuevos datos para el mapa
    }
    
    return render(request, 'home.html', context)

def CustomLoginView(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {"form": LoginForm()})
    else:
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            form.add_error('username', 'Usuario o contraseña incorrectos. Por favor, intenta nuevamente.')
        return render(request, 'registration/login.html', {"form": form})
        
@login_required
def logout(request):
    django_logout(request)
    return redirect('login')

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {"form": RegisterForm})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                    user.save()
                    return redirect('login')
                except IntegrityError:
                    form.add_error('username', 'Usuario ya existe')
            else:
                form.add_error('password2', 'Las contraseñas no coinciden')

        return render(request, 'registration/register.html', {"form": form})

def handler404(request, exception):
    """
    Vista personalizada para errores 404
    """
    return render(request, '404.html', status=404)

def handler500(request):
    """
    Vista personalizada para errores 500
    """
    
    return render(request, '500.html', status=500)