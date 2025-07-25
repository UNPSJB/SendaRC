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
from django.db.models import Q, Count, Sum
from .models import Factura
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from .models import Factura, Detalle_Servicios, Detalle_Empleados
from django.http import JsonResponse
import logging
import traceback


@login_required
def facturas(request):
    today = timezone.now().date()
    # Fetch the 5 unpaid invoices with valid due dates, closest to their due date
    facturas_proximas_vencer = (
        Factura.objects.filter(fechaPago__isnull=True, fecha_vencimiento__isnull=False)
        .select_related("cliente", "servicio")
        .order_by("fecha_vencimiento")[:5]
    )

    # Add dias_para_vencer, due_text, and due_class to each factura
    for factura in facturas_proximas_vencer:
        factura.dias_para_vencer = (factura.fecha_vencimiento - today).days
        if factura.dias_para_vencer == 0:
            factura.due_text = "Vence hoy"
            factura.due_class = "due-urgent"
        elif factura.dias_para_vencer == 1:
            factura.due_text = "Vence mañana"
            factura.due_class = "due-urgent"
        elif factura.dias_para_vencer < 0:
            abs_days = abs(factura.dias_para_vencer)
            factura.due_text = (
                f"Vencida hace {abs_days} día{'s' if abs_days != 1 else ''}"
            )
            factura.due_class = "due-urgent"
        else:
            factura.due_text = f"{factura.dias_para_vencer} día{'s' if factura.dias_para_vencer != 1 else ''}"
            factura.due_class = (
                "due-urgent"
                if factura.dias_para_vencer <= 3
                else "due-warning" if factura.dias_para_vencer <= 7 else "due-normal"
            )

    context = {
        "facturas_proximas_vencer": facturas_proximas_vencer,
    }
    return render(request, "factura/facturas.html", context)

@login_required
def verFacturas(request):
    # Si es una petición AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return get_facturas_ajax(request)
    
    
    # Para la carga inicial de la página
    context = get_facturas_context(request)
    return render(request, "factura/verFacturas.html", context)

def get_facturas_context(request):
    """Función auxiliar para obtener el contexto de facturas"""
    # Obtener parámetros de los filtros
    filters = {
        'search_query': request.GET.get("search", "").strip(),
        'tipo': request.GET.get("tipo", ""),
        'estado': request.GET.get("estado", ""),
        'fecha_emision_desde': request.GET.get("fecha_emision_desde", ""),
        'fecha_emision_hasta': request.GET.get("fecha_emision_hasta", ""),
        'fecha_vencimiento_desde': request.GET.get("fecha_vencimiento_desde", ""),
        'fecha_vencimiento_hasta': request.GET.get("fecha_vencimiento_hasta", ""),
        'periodo_servicio': request.GET.get("periodo_servicio", "").strip(),
    }
    
    # Obtener todas las facturas con optimización de consultas
    facturas = Factura.objects.select_related('cliente', 'servicio').all()
    today = timezone.now().date()
    
    # Aplicar filtros
    facturas = apply_filters(facturas, filters, today)
    
    # Calcular estadísticas (antes de la paginación)
    stats = calculate_statistics(facturas, today)

    
    # Ordenamiento - solo si hay resultados
    sort_by = request.GET.get('sort', '-fechaEmision')
    if facturas.exists():  # Verificar que hay facturas antes de ordenar
        if sort_by in ['-fechaEmision', 'fechaEmision', '-importe', 'importe', '-fecha_vencimiento', 'fecha_vencimiento']:
            facturas = facturas.order_by(sort_by)
        else:
            facturas = facturas.order_by('-fechaEmision')
    
    # Paginación
    per_page = min(int(request.GET.get('per_page', 10)), 100)  # Máximo 100 por página
    paginator = Paginator(facturas, per_page)
    page_number = request.GET.get("page", 1)
    
    try:
        facturas_page = paginator.get_page(page_number)
    except Exception as e:
        # Si hay error en paginación, devolver página 1
        facturas_page = paginator.get_page(1)
    
    context = {
        "facturas": facturas_page,
        "today": today,
        "filters": filters,
        **stats
    }
    
    return context

def apply_filters(facturas, filters, today):
    """Aplicar todos los filtros a la queryset"""
    try:
        if filters['search_query']:
            facturas = facturas.filter(
                Q(cliente__nombre__icontains=filters['search_query']) |
                Q(cliente__apellido__icontains=filters['search_query']) |
                Q(servicio__id__icontains=filters['search_query']) |
                Q(id__icontains=filters['search_query'])
            )
        if filters['periodo_servicio']:
            facturas = facturas.filter(periodoServicio=int(filters['periodo_servicio']))

        if filters['tipo']:
            facturas = facturas.filter(tipo=filters['tipo'])
        
        if filters['estado']:
            if filters['estado'] == "pagada":
                facturas = facturas.filter(fechaPago__isnull=False)
            elif filters['estado'] == "pendiente":
                facturas = facturas.filter(
                    fechaPago__isnull=True, 
                    fecha_vencimiento__gte=today
                )
            elif filters['estado'] == "vencida":
                facturas = facturas.filter(
                    fechaPago__isnull=True, 
                    fecha_vencimiento__lt=today
                )
        
        # Filtros de fecha con validación
        if filters['fecha_emision_desde']:
            try:
                fecha_desde = datetime.strptime(filters['fecha_emision_desde'], '%Y-%m-%d').date()
                facturas = facturas.filter(fechaEmision__gte=fecha_desde)
            except (ValueError, TypeError):
                pass  # Ignorar fecha inválida
        
        if filters['fecha_emision_hasta']:
            try:
                fecha_hasta = datetime.strptime(filters['fecha_emision_hasta'], '%Y-%m-%d').date()
                facturas = facturas.filter(fechaEmision__lte=fecha_hasta)
            except (ValueError, TypeError):
                pass  # Ignorar fecha inválida
        
        if filters['fecha_vencimiento_desde']:
            try:
                fecha_desde = datetime.strptime(filters['fecha_vencimiento_desde'], '%Y-%m-%d').date()
                facturas = facturas.filter(fecha_vencimiento__gte=fecha_desde)
            except (ValueError, TypeError):
                pass  # Ignorar fecha inválida
        
        if filters['fecha_vencimiento_hasta']:
            try:
                fecha_hasta = datetime.strptime(filters['fecha_vencimiento_hasta'], '%Y-%m-%d').date()
                facturas = facturas.filter(fecha_vencimiento__lte=fecha_hasta)
            except (ValueError, TypeError):
                pass  # Ignorar fecha inválida
        
    except Exception as e:
        # Log del error para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error aplicando filtros: {str(e)}")
        # Devolver queryset vacío en caso de error
        return Factura.objects.none()
    
    return facturas

def calculate_statistics(facturas, today):
    """Calcular estadísticas de las facturas filtradas"""
    try:
        # Usar agregaciones para mejor performance
        stats = facturas.aggregate(
            total_count=Count('id'),
            total_amount=Sum('importe'),
            pagadas_count=Count('id', filter=Q(fechaPago__isnull=False)),
            pendientes_count=Count('id', filter=Q(fechaPago__isnull=True, fecha_vencimiento__gte=today)),
            vencidas_count=Count('id', filter=Q(fechaPago__isnull=True, fecha_vencimiento__lt=today)),
        )
        
        return {
            'total_facturas': stats['total_count'] or 0,
            'facturas_pagadas': stats['pagadas_count'] or 0,
            'facturas_pendientes': stats['pendientes_count'] or 0,
            'facturas_vencidas': stats['vencidas_count'] or 0,
            'total_amount': stats['total_amount'] or 0,
        }
    except Exception as e:
        # Log del error y devolver estadísticas vacías
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error calculando estadísticas: {str(e)}")
        
        return {
            'total_facturas': 0,
            'facturas_pagadas': 0,
            'facturas_pendientes': 0,
            'facturas_vencidas': 0,
            'total_amount': 0,
        }

def get_facturas_ajax(request):
    """Función para manejar peticiones AJAX"""
    try:
        context = get_facturas_context(request)
        
        # Renderizar solo las partes que necesitan actualizarse
        try:
            stats_html = render_to_string('factura/partials/stats_section.html', context, request=request)
        except Exception as e:
            stats_html = f'<div class="alert alert-warning">Error cargando estadísticas: {str(e)}</div>'
        
        try:
            table_html = render_to_string('factura/partials/table_section.html', context, request=request)
        except Exception as e:
            table_html = '<div class="alert alert-warning">Error cargando tabla</div>'
        
        try:
            pagination_html = render_to_string('factura/partials/pagination_section.html', context, request=request)
        except Exception as e:
            pagination_html = ''
        
        return JsonResponse({
            'success': True,
            'stats_html': stats_html,
            'table_html': table_html,
            'pagination_html': pagination_html,
            'total_count': context['total_facturas'],
            'stats': {
                'total': context['total_facturas'],
                'pagadas': context['facturas_pagadas'],
                'pendientes': context['facturas_pendientes'],
                'vencidas': context['facturas_vencidas'],
                'total_amount': float(context['total_amount']) if context['total_amount'] else 0.0,
            }
        })
    
    except Exception as e:
        # Log detallado del error
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error en get_facturas_ajax: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)


@login_required
def serviciosFacturar(request):
    fecha_actual = timezone.now().date()
    ultimo_dia_mes = timezone.now().date() + timedelta(
        days=(32 - timezone.now().date().day)
    )
    fecha_limite = ultimo_dia_mes - timedelta(days=10)
    servicios = []

    if request.method == "GET":
        if len(request.GET) > 0:
            form = SelectClienteForm(request.GET)
            cliente = Cliente.habilitados.get(pk=request.GET.get("cliente", ""))

            # Logica para servicios contratados y eventuales, ya son los unicos que se van a poder generar facturas cuando estan contratados
            servicios_contratados = Servicio.objects.filter(estado=3, cliente=cliente)
            for servicio in servicios_contratados:
                # Eventuales facturar antes de iniciar el servicio,
                if servicio.tipo == 1 and fecha_actual < servicio.fecha_inicio:
                    if (
                        cliente.tipo == 1
                        and len(Factura.objects.filter(servicio=servicio)) < 2
                    ):
                        servicios.append(servicio)
                    elif (
                        cliente.tipo == 2
                        and len(Factura.objects.filter(servicio=servicio)) < 1
                    ):
                        servicios.append(servicio)

            # Logica para servicios en curso y determinados, ya son los unicos que se van a poder generar facturas cuando estan en curso
            if fecha_actual <= ultimo_dia_mes and fecha_actual >= fecha_limite:
                # Logica para servicios en curso y determinados, ya que son los unicos que se van a poder generar factura si estan en curso
                servicios_en_curso = Servicio.objects.filter(estado=4, cliente=cliente)
                for servicio in servicios_en_curso:
                    # Determinados facturar los ultimos dias del mes en el que se realizo el servicio
                    if (
                        servicio.tipo == 2
                        and fecha_actual >= servicio.fecha_inicio
                        and fecha_actual <= servicio.fecha_finaliza
                    ):
                        servicio_facturas = Factura.objects.filter(servicio=servicio)
                        for factura in servicio_facturas:
                            if (
                                factura.periodoServicio != fecha_actual.month
                                or factura.tipo == 1
                            ):
                                servicios.append(servicio)
        else:
            form = SelectClienteForm()

    return render(
        request,
        "factura/serviciosFacturar.html",
        {"form": form, "servicios": servicios},
    )


@login_required
def generarFactura(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    fecha_actual = timezone.now().date()
    print("-------------EN GENERAR FACTURA, MES:", fecha_actual.month)
    if fecha_actual.month == 12:
        primer_dia_next_mes = fecha_actual.replace(day=1, month=1)
    else:
        primer_dia_next_mes = fecha_actual.replace(day=1, month=fecha_actual.month + 1)

    # Fecha emision no asignamos nada por su atributo que pusimos en el model Frecuencia
    factura = Factura(
        fecha_vencimiento=primer_dia_next_mes.replace(day=10),
        cliente=servicio.cliente,
        servicio=servicio,
    )

    # Logica cuando es servicio eventual y cliente ocasional o habitual
    if servicio.tipo == 1 and servicio.cliente.tipo == 1:
        factura.importe = servicio.importe_total * 0.5  # calculo para el 50%
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
            factura.importe = servicio.importe_total * 0.5  # calculo para el 50%
            factura.tipo = 3
        factura.periodoServicio = fecha_actual.month
    elif servicio.tipo == 2 and servicio.cliente.tipo == 2:
        factura.importe = servicio.importe_total
        factura.tipo = 3
        factura.periodoServicio = fecha_actual.month

    factura.save()

    servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(
        servicio=servicio
    )
    for tipo in servicio_tipos_servicios:
        tipo_servicio = TipoServicio.habilitados.get(pk=tipo.tipoServicio.pk)
        Detalle_Servicios.objects.create(
            factura=factura,
            tipo_servicio=tipo_servicio.descripcion,
            tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
            precio_tipo_servicio=tipo_servicio.precio,
            cantidad=tipo.cantidad,
        )

    if servicio.tipo == "Determinado":
        cant_empleados = (
            len(Frecuencia.objects.filter(servicio=servicio))
            * servicio.cant_empleados
            * 4
        )
    else:
        cant_empleados = (
            len(Frecuencia.objects.filter(servicio=servicio)) * servicio.cant_empleados
        )
    mano_obra = Empleado.getSueldoBasico() / 24
    Detalle_Empleados.objects.create(
        factura=factura,
        cantidad_empleados=servicio.cant_empleados,
        importe_mano_obra=(mano_obra * cant_empleados),
    )

    return redirect("facturaRegistrada", factura.pk)


@login_required
def facturaRegistrada(request, pk):
    factura = Factura.objects.get(pk=pk)
    return render(request, "factura/facturaRegistrada.html", {"factura": factura})


@method_decorator(login_required, name="dispatch")
class serviciosCobrar(ListView):
    model = Servicio
    template_name = "factura/serviciosCobrar.html"
    context_object_name = "servicios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context["form"] = SelectClienteForm(self.request.GET)
        else:
            context["form"] = SelectClienteForm()
        return context

    def get_queryset(self):
        queryset = Servicio.objects.filter(estado__in=[3, 4, 5])
        cliente = self.request.GET.get("cliente", "")
        if cliente:
            queryset = queryset.filter(cliente=cliente)
        else:
            queryset = None
        return queryset


@login_required
def detalleServicioFactura(request, pk):
    servicio = Servicio.objects.get(id=pk)
    return render(
        request, "factura/detalleServicioFactura.html", {"servicio": servicio}
    )


@login_required
def facturasServicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    facturas = Factura.objects.filter(servicio=servicio)

    return render(request, "factura/facturasServicio.html", {"facturas": facturas})


@login_required
def detalleFactura(request, pk):
    # Fetch the Factura instance
    factura = get_object_or_404(
        Factura.objects.select_related("cliente", "servicio"), pk=pk
    )

    # Fetch related DetalleServicio instances, if any
    detalles_servicios = Detalle_Servicios.objects.filter(factura=factura)

    # Compute subtotal for each DetalleServicio
    for detalle in detalles_servicios:
        detalle.subtotal = detalle.precio_tipo_servicio * detalle.cantidad
        detalle.subtotal_formateado = f"${detalle.subtotal:,.0f}".replace(",", ".")
        detalle.precio_tipo_servicio_formateado = (
            f"${detalle.precio_tipo_servicio:,.0f}".replace(",", ".")
        )

    # Fetch related DetalleEmpleado instance, if any
    detalle_empleado = Detalle_Empleados.objects.filter(factura=factura).first()

    context = {
        "factura": factura,
        "detalles_servicios": detalles_servicios,
        "detalle_empleado": detalle_empleado,
    }

    return render(request, "factura/detalleFactura.html", context)


@login_required
def formaPago(request, pk):
    factura = Factura.objects.get(pk=pk)
    form = FormaPagoForm()

    if request.method == "POST":
        form = FormaPagoForm(request.POST)
        if form.is_valid():
            tipo_pago = form.cleaned_data["forma"]
            factura.fechaPago = timezone.now().date()
            if tipo_pago == "Efectivo":
                factura.formaPago = 1
            else:
                factura.formaPago = 3

            factura.save()
            return redirect("verFacturas")
        else:
            print(form.errors)
    else:
        print(factura)

    return render(
        request,
        "factura/formaPago.html",
        {"form": form, "factura": factura, "servicio": factura.servicio},
    )


@login_required
def crearFacturaSeña(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    cliente = servicio.cliente
    mitad_importe = servicio.importe_total * 0.50

    factura_seña = Factura.objects.create(
        servicio=servicio,
        importe=mitad_importe,
        cliente=cliente,
        tipo=1,
        fechaEmision=datetime.now(),
    )

    return redirect("detallesFacturaSeña", pk=factura_seña.pk)


@login_required
def detallesFacturaSeña(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    return render(
        request, "factura/detallesFacturaSeña.html", {"factura_seña": factura_seña}
    )


@login_required
def realizarCobroFacturaSeña(request, pk):
    if request.method == "POST":
        servicio = get_object_or_404(Servicio, pk=pk)
        cliente = servicio.cliente
        mitad_importe = servicio.importe_total * 0.50

        # Crear la factura seña
        factura_seña = Factura.objects.create(
            servicio=servicio,
            importe=mitad_importe,
            cliente=cliente,
            tipo=1,  # Seña
            fechaEmision=datetime.now(),
        )

        # ERROR CORREGIDO: Esta línea estaba mal, estás usando pk del servicio, no de la factura
        # factura_seña = Factura.objects.get(pk=pk)  # ❌ INCORRECTO
        # La factura ya está creada arriba, no necesitas hacer otro get

        form = FormCobroFacturaSeña(request.POST)
        if form.is_valid():
            factura_seña.formaPago = form.cleaned_data["formapago"]
            factura_seña.fechaPago = datetime.now()
            factura_seña.save()

            # Actualizar el estado del servicio
            servicio.estado = 3
            servicio.save()

            print("servicio.pk", servicio.pk)

            # AQUÍ SE EJECUTA LA FUNCIÓN QUE CREA LA FACTURA RESTANTE
            return redirect("contratarServicioCorrecto", servicio.pk)
        else:
            print(form.errors)
            # ERROR CORREGIDO: Faltaba el template en el render
            return render(
                request,
                "factura/CobroFacturaSeña.html",
                {"servicio": servicio, "facturaSeña": factura_seña, "form": form},
            )

    # GET request - mostrar el formulario
    servicio = get_object_or_404(Servicio, pk=pk)

    # Verificar si ya existe una factura seña para este servicio
    try:
        facturaSeña = Factura.objects.get(servicio=servicio, tipo=1)
    except Factura.DoesNotExist:
        # Si no existe, crear un objeto temporal para mostrar la información
        # sin guardarlo en la base de datos
        mitad_importe = servicio.importe_total * 0.50
        facturaSeña = Factura(
            servicio=servicio,
            importe=mitad_importe,
            cliente=servicio.cliente,
            tipo=1,
            fechaEmision=datetime.now().date(),
        )

    form = FormCobroFacturaSeña()
    context = {"servicio": servicio, "facturaSeña": facturaSeña, "form": form}
    return render(request, "factura/CobroFacturaSeña.html", context)


@login_required
def facturaPagada(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    context = {"factura_seña": factura_seña}
    return render(request, "factura/facturaSeñaPagada.html", context)


@login_required
def generar_pdf_factura(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    servicio = factura.servicio
    cliente = factura.cliente
    detalle_servicios_qs = Detalle_Servicios.objects.filter(factura=factura)
    detalle_empleados = Detalle_Empleados.objects.filter(factura=factura).first()
    importe_total_servicios = 0

    if factura.tipo != 1:
        detalle_servicios = []
        for item in detalle_servicios_qs:
            subtotal = item.precio_tipo_servicio * item.cantidad
            subtotal_formateado = f"${subtotal:,.0f}".replace(",", ".")
            precio_unitario_formateado = f"${item.precio_tipo_servicio:,.0f}".replace(
                ",", "."
            )

            detalle_servicios.append(
                {
                    "descripcion": item.tipo_servicio,
                    "unidad": item.tipo_servicio_Unit,
                    "precio_unitario": precio_unitario_formateado,
                    "cantidad": item.cantidad,
                    "subtotal": subtotal_formateado,
                }
            )
            importe_total_servicios += subtotal

        importe_total_servicios_formateado = f"${importe_total_servicios:,.0f}".replace(
            ",", "."
        )

    # Obtener facturas asociadas al mismo servicio, excluyendo la actual, y que estén pagadas
    facturas_restantes = Factura.objects.filter(servicio=servicio).exclude(
        fechaPago__isnull=False
    )
    print("facturas_restantes", facturas_restantes)
    facturas_restantes_count = facturas_restantes.count()
    print("facturas_restantes_count", facturas_restantes_count)

    context = {
        "factura": factura,
        "cliente": cliente,
        "servicio": servicio,
        "detalle_servicios": detalle_servicios if factura.tipo != 1 else [],
        "detalle_empleados": detalle_empleados if factura.tipo != 1 else [],
        "subtotal": subtotal if factura.tipo != 1 else 0,
        "importe_total_servicios": (
            importe_total_servicios_formateado if factura.tipo != 1 else 0
        ),
        "facturas_restantes": facturas_restantes_count,
    }

    template = get_template("factura/pdfFactura.html")
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=factura_{factura.pk}.pdf"

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")), dest=response, encoding="UTF-8"
    )
    if pisa_status.err:
        return HttpResponse("Hubo un error al generar el PDF", status=500)
    return response
