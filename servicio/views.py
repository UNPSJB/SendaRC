from typing import Any, Self
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django import forms
from core.models import *
from factura.models import Detalle_Empleados, Detalle_Servicios, Factura
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from dateutil.relativedelta import relativedelta
from .forms import FormBaseFrecuencia
import json
from .models import Frecuencia

dias_json = json.dumps([{"value": d[0], "label": d[1]} for d in Frecuencia.DIA])
turnos_json = json.dumps([{"value": t[0], "label": t[1]} for t in Frecuencia.TURNO])

FrecuenciaFormSet = formset_factory(
    FormBaseFrecuencia, extra=0, can_delete=True
)  # extra=0 porque agregamos por JS


def formato_moneda(valor):
    return (
        "${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    )


def calcularPorcentaje(total_importe, porcentaje):
    cambio = (porcentaje / 100) * total_importe
    total_importe = total_importe + cambio
    return total_importe


def calcularImportePresupuesto(listaTipoServicio, cantEmpleados, cantFrecuencias, tipo):
    importe_sugerido = 0
    dicc_total_importe = {}
    tipos_servicios_precios = 0

    print("\n▶️ INICIO del cálculo")
    print(f"- Tipo de contrato: {tipo}")
    print(f"- Cantidad de frecuencias: {cantFrecuencias}")
    print(f"- Cantidad de empleados por turno: {cantEmpleados}\n")

    # Recorremos cada tipo de servicio
    for item in listaTipoServicio:
        precio_item = item["tipo_servicio"].getPrecio(item["cantidad"])
        tipos_servicios_precios += precio_item
        print(f"• Tipo de servicio: {item['tipo_servicio']}")
        print(f"  - Cantidad: {item['cantidad']}")
        print(f"  - Precio por cantidad: {precio_item}\n")

    print(f"💰 Precio total por turno: {tipos_servicios_precios}")

    # Total de los servicios que se hacen todos los turnos
    total_servicios = tipos_servicios_precios * cantFrecuencias
    dicc_total_importe["total_servicios"] = total_servicios
    print(
        f"💰 Precio total por todos los turnos (x{cantFrecuencias}): {total_servicios}"
    )

    # Calculamos empleados totales
    if tipo == 2:
        cant_empleados = cantFrecuencias * cantEmpleados * 4
        print(f"👷 Empleados calculados (Determinado): {cant_empleados}")
    else:
        cant_empleados = cantFrecuencias * cantEmpleados
        print(f"👷 Empleados calculados (Eventual): {cant_empleados}")

    mano_obra_unitaria = Empleado.getSueldoBasico() / 24
    print(f"🛠️ Mano de obra por empleado (mensual/24): {mano_obra_unitaria}")

    total_mano_obra = mano_obra_unitaria * cant_empleados
    print(f"🛠️ Costo total de mano de obra: {total_mano_obra}")

    importe_sugerido = 1.15 * total_servicios + total_mano_obra
    ganancia = 0.15 * total_servicios

    print(f"📈 Ganancia 15% sobre servicios: {ganancia}")
    print(f"💵 Importe sugerido (ganancia + mano de obra): {importe_sugerido}")

    # Guardamos en el diccionario
    dicc_total_importe["porcentaje_ganancia"] = ganancia
    dicc_total_importe["mano_obra_servicio"] = total_mano_obra
    dicc_total_importe["importe_sugerido"] = importe_sugerido

    print("\n✅ Resultado final:")
    for clave, valor in dicc_total_importe.items():
        print(f"  {clave}: {valor}")

    return dicc_total_importe


def saveServicio(datos_cliente, form_data, total, servicio_pk):
    new_servicio = None

    # Get the Localidad instance if localidad is provided
    localidad_instance = None
    if datos_cliente.get("localidad"):
        try:
            # If localidad is a pk (integer), get the instance
            if isinstance(datos_cliente["localidad"], int):
                localidad_instance = Localidad.objects.get(
                    pk=datos_cliente["localidad"]
                )
            # If localidad is already an instance, use it directly
            elif hasattr(datos_cliente["localidad"], "pk"):
                localidad_instance = datos_cliente["localidad"]
            # If localidad is a string representation of pk
            else:
                localidad_instance = Localidad.objects.get(
                    pk=int(datos_cliente["localidad"])
                )
        except (Localidad.DoesNotExist, ValueError, TypeError):
            # Handle the case where localidad doesn't exist or conversion fails
            localidad_instance = None

    if servicio_pk == None:
        new_servicio = Servicio(
            plazo_vigencia=timezone.now() + timedelta(days=10),
            cliente=Cliente.objects.get(pk=datos_cliente["cliente_pk"]),
            direccion=datos_cliente["direccion"],
            metros2=datos_cliente["metros2"],
            observaciones=datos_cliente["observaciones"],
            cant_empleados=form_data["cantidad_empleados"],
            porcentaje=form_data["porcentaje"],
            tipo=datos_cliente["tipo"],
            estado=1,
            importe_total=total,
            localidad=localidad_instance,
        )
        new_servicio.save()
    else:
        print("-------ELSE PARA MODIFICAR ")
        new_servicio = Servicio.objects.get(pk=servicio_pk)
        new_servicio.cliente = Cliente.objects.get(pk=datos_cliente["cliente_pk"])
        new_servicio.direccion = datos_cliente["direccion"]
        new_servicio.metros2 = datos_cliente["metros2"]
        new_servicio.observaciones = datos_cliente["observaciones"]
        new_servicio.cant_empleados = form_data["cantidad_empleados"]
        new_servicio.porcentaje = form_data["porcentaje"]
        new_servicio.tipo = datos_cliente["tipo"]
        new_servicio.estado = 1
        new_servicio.importe_total = total
        new_servicio.localidad = localidad_instance
        new_servicio.save()
    return new_servicio


def saveTipoServicios(servicio, listTipoServicio, servicio_pk):
    if servicio_pk != None:
        CantServicioTipoServicio.objects.filter(servicio=servicio).delete()

    for tipo in listTipoServicio:
        new_servicio_tipo_servicio = CantServicioTipoServicio.objects.create(
            servicio=servicio,
            tipoServicio=TipoServicio.objects.get(pk=tipo["tipo_servicio"].pk),
            cantidad=tipo["cantidad"],
        )


def saveFrecuenca(servicio, listFrecuencias, servicio_pk):
    if servicio_pk != None:
        Frecuencia.objects.filter(servicio=servicio).delete()

    for frecuencia in listFrecuencias:
        dia_num = next(
            (key for key, value in Frecuencia.DIA if value == frecuencia["dia"]), None
        )
        turno_num = next(
            (key for key, value in Frecuencia.TURNO if value == frecuencia["turno"]),
            None,
        )
        Frecuencia.objects.create(dia=dia_num, turno=turno_num, servicio=servicio)
        # new_frecuencia = Frecuencia.objects.create(dia=dia_num, turno=turno_num, servicio=servicio)


def recargarSession(servicio, presupuestoSession):
    # Cargamos los datos del cliente que ya estaban
    datos_cliente = {
        "direccion": servicio.direccion,
        "metros2": servicio.metros2,
        "observaciones": servicio.observaciones,
        "tipo": servicio.tipo,
        "cliente": servicio.cliente,
        "localidad": servicio.localidad,
    }  # Agregar localidad
    presupuestoSession.update(datos_cliente)
    presupuestoSession.store()
    # Cargamos la lista de tipos de servicio del servicio a modificar
    lista_tipos_servicio = CantServicioTipoServicio.objects.filter(servicio=servicio)
    for tipo_servicio in lista_tipos_servicio:
        tipo_servicio_data = {
            "tipo_servicio": tipo_servicio.tipoServicio,
            "cantidad": tipo_servicio.cantidad,
        }
        presupuestoSession.update(tipo_servicio_data)
        presupuestoSession.storeServicio()
    # Cargamos la lista de frecuencias del servicio a modificar
    lista_frecuencias = Frecuencia.objects.filter(servicio=servicio)
    for frecuencia in lista_frecuencias:
        frecuencia_data = {"dia": frecuencia.dia, "turno": frecuencia.turno}
        presupuestoSession.update(frecuencia_data)
        presupuestoSession.storeFrecuencia()
    # Debemos devolver el presupuestoSession ? creo que no
    # return presupuestoSession


class PresupuestoSession(dict):
    FIELDS = [
        "direccion",
        "metros2",
        "observaciones",
        "tipo",
        "localidad",
    ]  # Agregar localidad

    # Create init for PresupuestoSession
    def __init__(self, session=None):
        self.session = session

    @classmethod
    def create(cls, session):
        return cls(session)

    @classmethod
    def getOrCreate(cls, session):
        p = PresupuestoSession.create(session)
        if "presupuesto" in session:
            p.update(session["presupuesto"])
        return p

    @classmethod
    def getTipoServicio(cls, session):
        listaS = []
        if "servicios" in session:
            listaS = session["servicios"]
        for item in listaS:
            item["tipo_servicio"] = TipoServicio.objects.get(pk=item["tipo_servicio"])
        return listaS

    @classmethod
    def getFrecuencia(cls, session):
        listaF = []
        MAP_DIA = dict(Frecuencia.DIA)
        MAP_TURNO = dict(Frecuencia.TURNO)
        if "frecuencias" in session:
            listaF = session["frecuencias"]
        for item in listaF:
            dia = int(item["dia"])
            item["dia"] = MAP_DIA.get(dia)
            turno = int(item["turno"])
            item["turno"] = MAP_TURNO.get(turno)
        return listaF

    def store(self):
        data = {k: v for k, v in self.items() if k in self.FIELDS}
        data["cliente_pk"] = self["cliente"].pk

        # Handle localidad field correctly
        if "localidad" in self and self["localidad"]:
            if hasattr(self["localidad"], "pk"):
                # If it's a Localidad instance, store the pk
                data["localidad"] = self["localidad"].pk
            else:
                # If it's already a pk or string, store it as is
                data["localidad"] = self["localidad"]
        else:
            data["localidad"] = None

        self.session["presupuesto"] = (
            data  # almacena todas la claves en la clave presupuesto de la session no ?
        )

    def storeServicio(self):
        data = self.session.get("servicios", [])
        servicio_data = {
            "tipo_servicio": self["tipo_servicio"].pk,
            "cantidad": self["cantidad"],
        }
        data.append(servicio_data)
        self.session["servicios"] = data

    def storeFrecuencia(self):
        data = self.session.get("frecuencias", [])
        frecuencia_data = {
            "dia": self["dia"],
            "turno": self["turno"],
        }
        data.append(frecuencia_data)
        self.session["frecuencias"] = data

    @property
    def cliente(self):
        if "cliente" not in self:
            self["cliente"] = Cliente.objects.get(pk=self["cliente_pk"])
        return self["cliente"]


@method_decorator(login_required, name="dispatch")
class gestionServicios(ListView):
    model = Servicio
    template_name = "servicio/gestionServicios.html"
    context_object_name = "servicios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltrosServiciosForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Servicio.objects.all()
        # Filtrar por estado
        estado_servicio = self.request.GET.get("estado", "")
        tipo_servicio = self.request.GET.get("tipo", "")

        if tipo_servicio:
            queryset = queryset.filter(tipo=tipo_servicio)
        if estado_servicio:
            queryset = queryset.filter(estado=estado_servicio)

        # Filtrar por fecha de inicio
        fecha_inicio = self.request.GET.get("fecha_inicio", "")
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio=fecha_inicio)
            print(queryset)
        # Filtrar por fecha de finalización
        fecha_finaliza = self.request.GET.get("fecha_finaliza", "")
        if fecha_finaliza:
            queryset = queryset.filter(fecha_finaliza=fecha_finaliza)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        self.request.session["presupuesto"] = {}
        self.request.session["servicios"] = []
        self.request.session["frecuencias"] = []
        self.request.session["servicio_pk"] = None
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "servicio/serviciosList.html", context, request=self.request
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)


@login_required
# vista que utiliza en canvas (modal) en la gestion para ver un miniResumen de un servicio
def canvasServicio(request, pk):
    servicio = Servicio.objects.get(id=pk)
    return render(request, "servicio/canvasServicio.html", {"servicio": servicio})


@login_required
def presupuestarCliente(request, pk=None):
    presupuesto_session = PresupuestoSession.getOrCreate(request.session)
    cliente = None
    if request.method == "POST":
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p = PresupuestoSession.getOrCreate(request.session)
            p.update(form.cleaned_data)  # Se guarda todos  los campos y sus valores
            p.store()
            return redirect("presupuestarServicios")
        else:
            print(form.errors)
    else:
        form = FormPresupuestoCliente()
        if pk:
            servicio = Servicio.objects.get(pk=pk)
            recargarSession(servicio, presupuesto_session)
            request.session["servicio_pk"] = pk
        else:
            request.session["servicio_pk"] = None
        dicc = request.session.get("presupuesto", {})
        if len(dicc) == 0:
            form = FormPresupuestoCliente()
        else:
            cliente = Cliente.habilitados.get(pk=dicc["cliente_pk"])
            form = FormPresupuestoCliente(
                initial={
                    "cliente": cliente,
                    "tipo": dicc["tipo"],
                    "direccion": dicc["direccion"],
                    "metros2": dicc["metros2"],
                    "observaciones": dicc["observaciones"],
                    "localidad": dicc["localidad"],
                }
            )

    return render(
        request, "servicio/presupuestarCliente.html", {"form": form, "cliente": cliente}
    )


@login_required
def presupuestarIdCliente(request, pk):
    presupuesto_session = PresupuestoSession.getOrCreate(request.session)
    cliente = Cliente.habilitados.get(pk=pk)

    if request.method == "POST":
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p = PresupuestoSession.getOrCreate(request.session)
            p.update(form.cleaned_data)
            p.store()
            return redirect("presupuestarServicios")
        else:
            print(form.errors)
    else:
        dicc = request.session.get("presupuesto", {})
        initial_data = presupuesto_session.session.get("presupuesto", {})
        initial_data["cliente"] = cliente.pk
        form = FormPresupuestoCliente(initial=initial_data)

    return render(
        request, "servicio/presupuestarCliente.html", {"form": form, "cliente": cliente}
    )


import json
from django.core.serializers import serialize


@login_required
def presupuestarServicios(request):
    p = PresupuestoSession.getOrCreate(request.session)

    if request.method == "POST":
        formset = formset_factory(FormBaseTipoServicio)
        formset = formset(request.POST)
        p.session["servicios"] = []
        print(formset)

        # Preparar tipos de servicio para el contexto (se usará en caso de error)
        tipos_servicio = TipoServicio.habilitados.all()
        tipos_servicio_json = json.dumps(
            [
                {
                    "id": tipo.id,
                    "descripcion": tipo.descripcion,
                    "unidad_medida": tipo.getUnidadMedida(),
                }
                for tipo in tipos_servicio
            ]
        )

        if formset.is_valid():
            # Contador de servicios válidos
            servicios_validos = 0
            formularios_con_errores = False

            for f in formset:
                cantidad = f.cleaned_data.get("cantidad", 0)
                tipo_servicio = f.cleaned_data.get(
                    "tipo_servicio"
                )  # Ajusta según tu modelo

                # Solo procesar si hay cantidad y tipo de servicio
                if cantidad > 0 and tipo_servicio:
                    if cantidad >= 300:
                        f.add_error(
                            "cantidad", "La cantidad no puede ser mayor o igual a 300."
                        )
                        formularios_con_errores = True
                    else:
                        servicios_validos += 1
                        p.update(f.cleaned_data)
                        p.storeServicio()

            # Verificar que haya al menos 1 servicio válido
            if servicios_validos == 0:
                # Agregar error no específico del campo (non_field_error)
                formset._non_form_errors = formset.error_class(
                    [
                        "Debe agregar al menos un tipo de servicio con cantidad mayor a 0."
                    ]
                )
                formularios_con_errores = True

            # Si hay errores, mostrar el formulario con errores
            if formularios_con_errores:
                return render(
                    request,
                    "servicio/presupuestarServicios.html",
                    {
                        "formset": formset,
                        "presupuesto": p,
                        "tipos_servicio": tipos_servicio,
                        "tipos_servicio_json": tipos_servicio_json,
                    },
                )

            # Si todo está bien, redirigir
            return redirect("presupuestarFrecuencias")
        else:
            print(formset.errors)
    else:
        lista = request.session.get("servicios", [])
        if len(lista) == 0:
            formset = formset_factory(FormBaseTipoServicio, extra=1)
        else:
            formset = formset_factory(FormBaseTipoServicio, extra=0)
            if "servicios" in p.session:
                formset = formset(initial=p.session["servicios"])

    # Preparar tipos de servicio para el contexto
    tipos_servicio = TipoServicio.habilitados.all()
    tipos_servicio_json = json.dumps(
        [
            {
                "id": tipo.id,
                "descripcion": tipo.descripcion,
                "unidad_medida": tipo.getUnidadMedida(),
            }
            for tipo in tipos_servicio
        ]
    )

    context = {
        "formset": formset,
        "presupuesto": p,
        "tipos_servicio": tipos_servicio,
        "tipos_servicio_json": tipos_servicio_json,
    }

    return render(request, "servicio/presupuestarServicios.html", context)


@login_required
def presupuestarFrecuencias(request):
    p = PresupuestoSession.getOrCreate(request.session)

    # Datos para el frontend
    dias_json = json.dumps([{"value": d[0], "label": d[1]} for d in Frecuencia.DIA])
    turnos_json = json.dumps([{"value": t[0], "label": t[1]} for t in Frecuencia.TURNO])

    if request.method == "POST":
        formset = FrecuenciaFormSet(request.POST)
        p.session["frecuencias"] = []
        dias_turnos = {}
        frecuencias_validas = 0

        if formset.is_valid():
            for f in formset:
                if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                    continue

                dia = f.cleaned_data["dia"]
                turno = f.cleaned_data["turno"]

                if dia not in dias_turnos:
                    dias_turnos[dia] = set()

                if dia in dias_turnos and len(dias_turnos[dia]) >= 3:
                    f.add_error("turno", "Un día solo puede tener 3 turnos distintos.")
                    return render(
                        request,
                        "servicio/presupuestarFrecuencia.html",
                        {
                            "formset": formset,
                            "presupuesto": p,
                            "dias_json": dias_json,
                            "turnos_json": turnos_json,
                        },
                    )

                if turno in dias_turnos[dia]:
                    f.add_error(
                        "turno", "No se permiten turnos duplicados para el mismo día."
                    )
                    return render(
                        request,
                        "servicio/presupuestarFrecuencia.html",
                        {
                            "formset": formset,
                            "presupuesto": p,
                            "dias_json": dias_json,
                            "turnos_json": turnos_json,
                        },
                    )

                dicc = p.session["presupuesto"]
                if dicc["tipo"] == 1 and len(dias_turnos) > 1:
                    f.add_error(
                        "dia", "Servicio eventual, solo 3 frecuencias, mismo día."
                    )
                    f.add_error(
                        "turno",
                        "Servicio eventual, solo 3 frecuencias, mismo día, turnos distintos.",
                    )
                    return render(
                        request,
                        "servicio/presupuestarFrecuencia.html",
                        {
                            "formset": formset,
                            "presupuesto": p,
                            "dias_json": dias_json,
                            "turnos_json": turnos_json,
                        },
                    )

                dias_turnos[dia].add(turno)
                p.update(f.cleaned_data)
                p.storeFrecuencia()
                frecuencias_validas += 1

            if frecuencias_validas == 0:
                formset.non_form_errors = lambda: [
                    "Debe ingresar al menos una frecuencia."
                ]
                return render(
                    request,
                    "servicio/presupuestarFrecuencia.html",
                    {
                        "formset": formset,
                        "presupuesto": p,
                        "dias_json": dias_json,
                        "turnos_json": turnos_json,
                    },
                )

            return redirect("presupuestarConfirmar")
        else:
            print(formset.errors)
            return render(
                request,
                "servicio/presupuestarFrecuencia.html",
                {
                    "formset": formset,
                    "presupuesto": p,
                    "dias_json": dias_json,
                    "turnos_json": turnos_json,
                },
            )
    else:
        lista = p.session.get("frecuencias", [])
        if lista:
            formset = FrecuenciaFormSet(initial=lista)
        else:
            formset = FrecuenciaFormSet(initial=[{}])

    return render(
        request,
        "servicio/presupuestarFrecuencia.html",
        {
            "formset": formset,
            "presupuesto": p,
            "dias_json": dias_json,
            "turnos_json": turnos_json,
        },
    )


@login_required
def presupuestarConfirmar(request):
    datos_cliente = PresupuestoSession.getOrCreate(request.session)
    tipos_servicios = PresupuestoSession.getTipoServicio(request.session)
    frecuencias = PresupuestoSession.getFrecuencia(request.session)
    servicio_pk = request.session.get("servicio_pk")

    print("DEBUG datos_cliente:", datos_cliente)

    # Inicializar todas las variables que se usan en el contexto del render
    importe_total = 0
    importe_sugerido = 0
    total_servicios = 0
    mano_obra = 0
    porcentaje_ganancia = 0
    importe_total_formateado = 0
    total_servicios_sin_formato = 0
    total_servicios_formateado = 0
    importe = {}

    def calcular_total_servicios_cantidad(tipos_servicios):
        total = 0
        for tipo in tipos_servicios:
            precio = tipo["tipo_servicio"].getPrecio(tipo["cantidad"])
            cantidad = tipo["cantidad"]
            total += precio
        return total

    if request.method == "POST":
        form = FormConfirmar(request.POST)
        if form.is_valid():
            if form.cleaned_data["cantidad_empleados"] <= 0:
                form.add_error(
                    "cantidad_empleados", "No se puede calcular con 0 o menos valores"
                )
                total_servicios_sin_formato = calcular_total_servicios_cantidad(
                    tipos_servicios
                )
                total_servicios_formateado = formato_moneda(total_servicios_sin_formato)

                return render(
                    request,
                    "servicio/presupuestarConfirmar.html",
                    {
                        "form": form,
                        "presupuesto": datos_cliente,
                        "tipo_Servicios": tipos_servicios,
                        "frecuencias": frecuencias,
                        "importe_sugerido": importe_sugerido,
                        "importe_total": importe_total,
                        "total_servicios_formateado": total_servicios_formateado,
                    },
                )
            new_servicio = saveServicio(
                datos_cliente,
                form.cleaned_data,
                form.cleaned_data["importe_total"],
                servicio_pk,
            )
            saveTipoServicios(new_servicio, tipos_servicios, servicio_pk)
            saveFrecuenca(new_servicio, frecuencias, servicio_pk)
            request.session["presupuesto"] = {}
            request.session["servicios"] = []
            request.session["frecuencias"] = []
            request.session["servicio_pk"] = None
            if servicio_pk == None:
                return redirect("presupuestarImprimir", new_servicio.pk)
            else:
                return redirect("presupuestarModificarImprimir", servicio_pk)
    else:
        # MODIFICADO: Manejo mejorado de peticiones GET (AJAX)
        if len(request.GET) > 0:
            form = FormConfirmar(request.GET)
            if int(request.GET.get("cantidad_empleados", 0)) >= 1:
                cant_empleados = int(request.GET["cantidad_empleados"])

                # Calcular importe base
                importe = calcularImportePresupuesto(
                    tipos_servicios,
                    cant_empleados,
                    len(frecuencias),
                    datos_cliente["tipo"],
                )

                # Aplicar porcentaje si existe
                porcentaje = int(request.GET.get("porcentaje", 0))
                if porcentaje != 0:
                    importe_total = calcularPorcentaje(
                        importe["importe_sugerido"], porcentaje
                    )
                else:
                    importe_total = importe["importe_sugerido"]
                # También devolver el nuevo valor de la mano de obra formateado
                mano_obra = formato_moneda(importe["mano_obra_servicio"])
                response_data = {
                    "importe_total": importe_total,
                    "mano_obra": mano_obra,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Debe ingresar al menos 1 empleado"})

        # Inicialización normal (no AJAX)
        elif servicio_pk != None:
            # Modo modificación
            servicio = Servicio.objects.get(pk=servicio_pk)
            form = FormConfirmar(
                initial={
                    "porcentaje": servicio.porcentaje,
                    "cantidad_empleados": servicio.cant_empleados,
                }
            )
            importe = calcularImportePresupuesto(
                tipos_servicios,
                servicio.cant_empleados,
                len(frecuencias),
                datos_cliente["tipo"],
            )
            importe_total = calcularPorcentaje(
                importe["importe_sugerido"], servicio.porcentaje
            )

            total_servicios = formato_moneda(importe["total_servicios"])
            porcentaje_ganancia = formato_moneda(importe["porcentaje_ganancia"])
            mano_obra = formato_moneda(importe["mano_obra_servicio"])
            importe_sugerido = "{:.2f}".format(importe["importe_sugerido"])
            importe_total_formateado = formato_moneda(importe_total)
            importe_total = "{:.2f}".format(importe_total)

            total_servicios_sin_formato = calcular_total_servicios_cantidad(
                tipos_servicios
            )
            total_servicios_formateado = formato_moneda(total_servicios_sin_formato)
        else:
            # Modo creación nuevo
            form = FormConfirmar()
            importe = calcularImportePresupuesto(
                tipos_servicios,
                form.fields["cantidad_empleados"].initial,
                len(frecuencias),
                datos_cliente["tipo"],
            )
            importe_total = importe["importe_sugerido"]
            total_servicios = formato_moneda(importe["total_servicios"])
            porcentaje_ganancia = formato_moneda(importe["porcentaje_ganancia"])
            mano_obra = formato_moneda(importe["mano_obra_servicio"])
            importe_sugerido = "{:.2f}".format(importe["importe_sugerido"])
            importe_total_formateado = formato_moneda(importe_total)
            importe_total = "{:.2f}".format(importe_total)

            total_servicios_sin_formato = calcular_total_servicios_cantidad(
                tipos_servicios
            )
            total_servicios_formateado = formato_moneda(total_servicios_sin_formato)

    return render(
        request,
        "servicio/presupuestarConfirmar.html",
        {
            "form": form,
            "presupuesto": datos_cliente,
            "tipo_Servicios": tipos_servicios,
            "frecuencias": frecuencias,
            "importe_sugerido": importe_sugerido,
            "importe_total": importe_total,
            "total_servicios": total_servicios,
            "mano_obra": mano_obra,
            "fecha_actual": timezone.now().date(),
            "importe_total_formateado": importe_total_formateado,
            "porcentaje_ganancia": porcentaje_ganancia,
            "total_servicios_formateado": total_servicios_formateado,
        },
    )


@login_required
def presupuestarImprimir(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    return render(request, "servicio/presupuestarImprimir.html", {"servicio": servicio})


@login_required
def detalleServicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    tipos_servicios = CantServicioTipoServicio.objects.filter(servicio=servicio)
    frecuencias = Frecuencia.objects.filter(servicio=servicio)

    empleados = Empleado.objects.filter(frecuencias__in=frecuencias).distinct()

    empleados_con_frecuencias = []
    for empleado in empleados:
        frecs = empleado.frecuencias.filter(servicio=servicio)
        empleados_con_frecuencias.append(
            {
                "empleado": empleado,
                "frecuencias": frecs,
            }
        )

    return render(
        request,
        "servicio/detalleServicio.html",
        {
            "servicio": servicio,
            "tipoServicios": tipos_servicios,
            "frecuencias": frecuencias,
            "empleados_con_frecuencias": empleados_con_frecuencias,
        },
    )


@login_required
def pdfImprimir(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    tipo_servicios = CantServicioTipoServicio.objects.filter(servicio=servicio)
    frecuencias = Frecuencia.objects.filter(servicio=servicio)

    # URL absoluta para la imagen
    img_url = request.build_absolute_uri(static("images/senda.png"))

    context = {
        "servicio": servicio,
        "tipoServicios": tipo_servicios,
        "frecuencias": frecuencias,
        "img_url": img_url,
    }

    # Cargar template
    template = get_template("servicio/pdfImprimir.html")
    html = template.render(context)

    # Crear respuesta HTTP como PDF
    response = HttpResponse(content_type="application/pdf")

    # Nombre del archivo según el tipo
    doc_type = "presupuesto" if servicio.estado in [1, 2] else "contrato"
    response["Content-Disposition"] = f"inline; filename={doc_type}_{servicio.pk}.pdf"

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response


@method_decorator(login_required, name="dispatch")
class contratarServicio(UpdateView):
    model = Servicio
    form_class = FormContratarServicio
    template_name = "servicio/contratarServicio.html"

    def get_success_url(self):
        return reverse_lazy("asignarEmpleados", kwargs={"pk": self.object.pk})

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()

        if self.object.estado != 1:
            return redirect("errorServicio")

        # Verificación de stock acumulado - CORREGIDO
        cant_serv_tipo = CantServicioTipoServicio.objects.filter(servicio=self.object)

        # Agrupar insumos necesarios por insumo
        insumos_requeridos = {}  # {insumo_id: cantidad_total_necesaria}

        for csts in cant_serv_tipo:
            tipo_servicio = csts.tipoServicio
            cantidad_tipo = csts.cantidad  # cuántas veces se requiere ese tipo

            # Busco todos los insumos necesarios para ese tipo de servicio
            insumos_necesarios = CantInsumoServicio.objects.filter(tipoServicio=tipo_servicio)

            for insumo_req in insumos_necesarios:
                insumo = insumo_req.insumo
                cantidad_unidad = insumo_req.cantidad  # cuánto necesita por 1 tipoServicio
                cantidad_total = cantidad_unidad * cantidad_tipo  # total necesaria para este tipo de servicio

                # Acumular la cantidad necesaria para este insumo
                if insumo.id in insumos_requeridos:
                    insumos_requeridos[insumo.id] += cantidad_total
                else:
                    insumos_requeridos[insumo.id] = cantidad_total

        # Verificar stock disponible para cada insumo
        errores_stock = []
        for insumo_id, cantidad_total_necesaria in insumos_requeridos.items():
            insumo = Insumo.objects.get(id=insumo_id)
            stock_disponible = insumo.cantidad or 0

            if stock_disponible < cantidad_total_necesaria:
                errores_stock.append(
                    f"Insumo '{insumo.descripcion}' insuficiente. "
                    f"Se necesitan {cantidad_total_necesaria}, hay {stock_disponible}"
                )

        if errores_stock:
            return render(request, "servicio/errorServicio.html", {
                "error": "No hay stock suficiente para contratar este servicio.",
                "detalle_errores": errores_stock
            })

        return super().get(request, *args, **kwargs)



@login_required
def contratarServicioCorrecto(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    cliente = servicio.cliente
    fecha_actual = timezone.now().date()
    cantInsumosServicios = CantInsumoServicio.objects.filter(tipoServicio__in=servicio.tipoServicios.all())

    if fecha_actual.month == 12:
        primer_dia_next_mes = fecha_actual.replace(
            day=1, month=1, year=fecha_actual.year + 1
        )
    else:
        primer_dia_next_mes = fecha_actual.replace(day=1, month=fecha_actual.month + 1)

    # EVENTUAL → crear factura restante después de la seña (Ocacional) o factura única (Habitual)
    if servicio.tipo == 1:  # Eventual
        if cliente.tipo == 1:  # Ocacional
            try:
                factura_seña = Factura.objects.get(servicio=servicio, tipo=1)
            except Factura.DoesNotExist:
                messages.error(request, "No se encontró la seña para este servicio.")
                return redirect("vista_servicio")

            # Verificamos que aún no se haya generado la factura restante
            if not Factura.objects.filter(servicio=servicio, tipo=2).exists():
                factura = Factura.objects.create(
                    fecha_vencimiento=primer_dia_next_mes.replace(day=10),
                    cliente=cliente,
                    servicio=servicio,
                    tipo=2,  # Única
                    periodoServicio=13,
                    importe=servicio.importe_total - factura_seña.importe,
                )

                # Crear detalles de servicios
                servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(
                    servicio=servicio
                )
                for tipo in servicio_tipos_servicios:
                    tipo_servicio = TipoServicio.habilitados.get(
                        pk=tipo.tipoServicio.pk
                    )
                    Detalle_Servicios.objects.create(
                        factura=factura,
                        tipo_servicio=tipo_servicio.descripcion,
                        tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
                        precio_tipo_servicio=tipo_servicio.precio,
                        cantidad=tipo.cantidad,
                    )

                # Crear detalle de empleados
                cant_empleados = (
                    len(Frecuencia.objects.filter(servicio=servicio))
                    * servicio.cant_empleados
                )
                mano_obra = Empleado.getSueldoBasico() / 24
                Detalle_Empleados.objects.create(
                    factura=factura,
                    cantidad_empleados=servicio.cant_empleados,
                    importe_mano_obra=(mano_obra * cant_empleados),
                )
        else:  # Habitual: paga todo junto (sin seña)
            if not Factura.objects.filter(servicio=servicio, tipo=2).exists():
                factura = Factura.objects.create(
                    fecha_vencimiento=primer_dia_next_mes.replace(day=10),
                    cliente=cliente,
                    servicio=servicio,
                    tipo=2,
                    periodoServicio=13,
                    importe=servicio.importe_total,
                )

                # Detalles de servicios
                servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(
                    servicio=servicio
                )
                for tipo in servicio_tipos_servicios:
                    tipo_servicio = TipoServicio.habilitados.get(
                        pk=tipo.tipoServicio.pk
                    )
                    Detalle_Servicios.objects.create(
                        factura=factura,
                        tipo_servicio=tipo_servicio.descripcion,
                        tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
                        precio_tipo_servicio=tipo_servicio.precio,
                        cantidad=tipo.cantidad,
                    )

                # Detalle de empleados
                cant_empleados = (
                    len(Frecuencia.objects.filter(servicio=servicio))
                    * servicio.cant_empleados
                )
                mano_obra = Empleado.getSueldoBasico() / 24
                Detalle_Empleados.objects.create(
                    factura=factura,
                    cantidad_empleados=servicio.cant_empleados,
                    importe_mano_obra=(mano_obra * cant_empleados),
                )

    # DETERMINADO → factura única restante (Ocacional) o facturas mensuales como cuotas (Habitual)
    elif servicio.tipo == 2:
        if cliente.tipo == 1:  # Ocacional
            try:
                factura_seña = Factura.objects.get(servicio=servicio, tipo=1)
            except Factura.DoesNotExist:
                messages.error(request, "No se encontró la seña para este servicio.")
                return redirect("vista_servicio")

            # Verificamos que aún no se haya generado la factura restante
            if not Factura.objects.filter(servicio=servicio, tipo=2).exists():
                factura = Factura.objects.create(
                    fecha_vencimiento=primer_dia_next_mes.replace(day=10),
                    cliente=cliente,
                    servicio=servicio,
                    tipo=2,  # Única
                    periodoServicio=13,
                    importe=servicio.importe_total - factura_seña.importe,
                )

                # Detalles de servicios
                servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(
                    servicio=servicio
                )
                for tipo in servicio_tipos_servicios:
                    tipo_servicio = TipoServicio.habilitados.get(
                        pk=tipo.tipoServicio.pk
                    )
                    Detalle_Servicios.objects.create(
                        factura=factura,
                        tipo_servicio=tipo_servicio.descripcion,
                        tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
                        precio_tipo_servicio=tipo_servicio.precio,
                        cantidad=tipo.cantidad,
                    )

                # Detalle de empleados
                cant_empleados = (
                    len(Frecuencia.objects.filter(servicio=servicio))
                    * servicio.cant_empleados
                    * 4
                )
                mano_obra = Empleado.getSueldoBasico() / 24
                Detalle_Empleados.objects.create(
                    factura=factura,
                    cantidad_empleados=servicio.cant_empleados,
                    importe_mano_obra=(mano_obra * cant_empleados),
                )
        else:  # Habitual
            fecha = servicio.fecha_inicio.replace(day=1)
            fecha_fin = servicio.fecha_finaliza.replace(day=1)
            # Calcular el número de meses
            meses = (
                (fecha_fin.year - fecha.year) * 12 + fecha_fin.month - fecha.month + 1
            )
            importe_mensual = (
                servicio.importe_total / meses if meses > 0 else servicio.importe_total
            )

            while fecha <= fecha_fin:
                vencimiento = (fecha + relativedelta(months=1)).replace(day=10)

                # Evitar duplicados
                if not Factura.objects.filter(
                    servicio=servicio, tipo=3, periodoServicio=fecha.month
                ).exists():
                    factura = Factura.objects.create(
                        fecha_vencimiento=vencimiento,
                        cliente=cliente,
                        servicio=servicio,
                        tipo=3,  # Mensual
                        periodoServicio=fecha.month,
                        importe=importe_mensual,
                    )

                    # Detalles de servicios
                    servicio_tipos_servicios = CantServicioTipoServicio.objects.filter(
                        servicio=servicio
                    )
                    for tipo in servicio_tipos_servicios:
                        tipo_servicio = TipoServicio.habilitados.get(
                            pk=tipo.tipoServicio.pk
                        )
                        Detalle_Servicios.objects.create(
                            factura=factura,
                            tipo_servicio=tipo_servicio.descripcion,
                            tipo_servicio_Unit=tipo_servicio.getUnidadMedida(),
                            precio_tipo_servicio=tipo_servicio.precio,
                            cantidad=tipo.cantidad,
                        )

                    # Detalles de empleados
                    cant_empleados = (
                        len(Frecuencia.objects.filter(servicio=servicio))
                        * servicio.cant_empleados
                        * 4
                    )
                    mano_obra = Empleado.getSueldoBasico() / 24
                    Detalle_Empleados.objects.create(
                        factura=factura,
                        cantidad_empleados=servicio.cant_empleados,
                        importe_mano_obra=(mano_obra * cant_empleados),
                    )

                fecha += relativedelta(months=1)

    # Cambiar estado del servicio a contratado
    servicio.estado = 3
    servicio.save()

    # DESCUENTO DE STOCK CORREGIDO - Agrupar por insumo
    cant_serv_tipo = CantServicioTipoServicio.objects.filter(servicio=servicio)
    
    # Agrupar insumos necesarios por insumo
    insumos_a_descontar = {}  # {insumo_id: cantidad_total_a_descontar}

    for csts in cant_serv_tipo:
        tipo_servicio = csts.tipoServicio
        cantidad_tipo = csts.cantidad

        # Busco todos los insumos necesarios para ese tipo de servicio
        insumos_necesarios = CantInsumoServicio.objects.filter(tipoServicio=tipo_servicio)

        for insumo_req in insumos_necesarios:
            insumo = insumo_req.insumo
            cantidad_unidad = insumo_req.cantidad
            cantidad_total = cantidad_unidad * cantidad_tipo

            # Acumular la cantidad a descontar para este insumo
            if insumo.id in insumos_a_descontar:
                insumos_a_descontar[insumo.id] += cantidad_total
            else:
                insumos_a_descontar[insumo.id] = cantidad_total

    # Realizar el descuento de stock una sola vez por insumo
    for insumo_id, cantidad_total_a_descontar in insumos_a_descontar.items():
        insumo = Insumo.objects.get(id=insumo_id)
        insumo.cantidad -= cantidad_total_a_descontar
        
        if insumo.cantidad <= 0:
            insumo.cantidad = 0
            insumo.activo = False
        
        insumo.save()

    return render(request, "servicio/contratarOpciones.html", {"servicio": servicio})


@method_decorator(login_required, name="dispatch")
class errorServicio(TemplateView):
    template_name = "servicio/errorServicio.html"


@login_required
def asignarEmpleados(request, pk):
    if request.method == "POST":
        formset_factory_cls = formset_factory(FormAsignarEmpleados)
        formset = formset_factory_cls(request.POST)
        servicio = Servicio.objects.get(pk=pk)

        if formset.is_valid():
            hay_errores = False
            for form in formset:
                frecuencia = form.cleaned_data["frecuencia"]
                empleados = form.cleaned_data["empleados"]
                if empleados.count() != servicio.cant_empleados:
                    form.add_error(
                        "empleados",
                        f"Se necesitan {servicio.cant_empleados} empleados por turno",
                    )
                    form.fields["empleados"].choices = [
                        (empleado.pk, f"{empleado.nombre} {empleado.apellido}")
                        for empleado in form.fields["empleados"].queryset
                    ]
                    hay_errores = True

            if hay_errores:
                return render(
                    request,
                    "servicio/asignarEmpleados.html",
                    {"formset": formset, "servicio": servicio},
                )

            # Si no hay errores, guardar datos
            for form in formset:
                frecuencia = form.cleaned_data["frecuencia"]
                empleados = form.cleaned_data["empleados"]
                frecuencia = Frecuencia.objects.get(pk=frecuencia.pk)
                for empleado in empleados:
                    frecuencia.empleados.add(empleado.pk)
                    servicio.empleado.add(empleado.pk)
                frecuencia.save()

            servicio.save()
            if servicio.cliente.tipo == 2:
                servicio.estado = 3
                servicio.save()
                return redirect("contratarServicioCorrecto", pk)
            

            return redirect("realizarCobroFacturaSeña", pk)

        # Si el formset no es válido (errores de validación base)
        return render(
            request,
            "servicio/asignarEmpleados.html",
            {"formset": formset, "servicio": servicio},
        )

    # GET request
    servicio = Servicio.objects.get(pk=pk)
    frecuencias = Frecuencia.objects.filter(servicio=servicio)
    formset_cls = formset_factory(FormAsignarEmpleados, extra=len(frecuencias))
    formset = formset_cls()

    for form, frecuencia in zip(formset, frecuencias):
        form.fields["frecuencia"].choices = [
            (
                frecuencia.pk,
                f"{frecuencia.get_dia_display()} - {frecuencia.get_turno_display()}",
            )
        ]
        form.fields["frecuencia"].initial = frecuencia.pk
        form.fields["empleados"].queryset = Empleado.habilitados.disponibles(
            servicio.fecha_inicio,
            servicio.fecha_finaliza,
            frecuencia.dia,
            frecuencia.turno,
        )
        form.fields["empleados"].choices = [
            (empleado.pk, f"{empleado.nombre} {empleado.apellido}")
            for empleado in form.fields["empleados"].queryset
        ]

    return render(
        request,
        "servicio/asignarEmpleados.html",
        {"formset": formset, "servicio": servicio},
    )

@login_required
def cancelar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    try:
        # Eliminar detalles relacionados a las facturas del servicio
        facturas = Factura.objects.filter(servicio=servicio)
        for factura in facturas:
            Detalle_Servicios.objects.filter(factura=factura).delete()
            Detalle_Empleados.objects.filter(factura=factura).delete()
        facturas.delete()

        # Eliminar frecuencias
        Frecuencia.objects.filter(servicio=servicio).delete()

        # Eliminar tipos de servicio intermedios
        CantServicioTipoServicio.objects.filter(servicio=servicio).delete()

        # Finalmente, eliminar el servicio
        servicio.delete()

        print(request, "El servicio fue cancelado correctamente.")
    except Exception as e:
        print(request, f"Ocurrió un error al cancelar el servicio: {str(e)}")

    return redirect("gestionServicios")  