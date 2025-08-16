import re
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from servicio.models import *
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from factura.models import Factura
import re
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.core.mail import EmailMultiAlternatives

@method_decorator(login_required, name="dispatch")
class altaCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/altaCliente.html"
    success_url = reverse_lazy("gestionClientes")

    def form_valid(self, form):
        cliente = form.save(commit=False)
        if not re.match("^[A-Za-z]+$", form.cleaned_data["nombre"]):
            form.add_error("nombre", "Solo se permite letras para el nombre.")
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data["apellido"]):
            form.add_error("apellido", "Solo se permite letras para el apellido.")
            return self.form_invalid(form)
        else:
            cliente.save()
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class gestionClientes(ListView):
    model = Cliente
    template_name = "cliente/gestionClientes.html"
    context_object_name = "clientes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroClientesForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Cliente.objects.all()

        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get("estado", "")
        if estado == "Activos" or not estado:
            queryset = Cliente.habilitados.all()
        elif estado == "No activos":
            queryset = Cliente.deshabilitados.all()

        # Filtrar por tipo de persona o tipo
        tipo_persona = self.request.GET.get("tipo_persona", "")
        if tipo_persona:
            queryset = queryset.filter(tipoPersona=tipo_persona)

        tipo = self.request.GET.get("tipo", "")
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "cliente/clientesList.html", context, request=self.request
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class updateCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/modificarCliente.html"
    success_url = reverse_lazy("gestionClientes")

    def get_form_kwargs(self):
        kwargs = super(updateCliente, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs

    def form_valid(self, form):
        cliente = form.save(commit=False)
        # Verificar si el cliente está asociado a servicios presupuestados, suspendidos, contratados o en curso
        servicios_asociados = Servicio.objects.filter(
            cliente=cliente, estado__in=[1, 3, 4, 5]
        )
        facturas_asociadas = Factura.objects.filter(cliente=cliente, fechaPago=None)

        if (
            form.cleaned_data["activo"] is False
            and len(servicios_asociados) > 0
            or len(facturas_asociadas) > 0
        ):
            form.add_error(
                "activo",
                "Error, el cliente tiene Servicios presupuestados, en curso,suspendidos o Facturas impagas.",
            )
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data["nombre"]):
            form.add_error("nombre", "Solo se permite letras para el nombre.")
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data["apellido"]):
            form.add_error("apellido", "Solo se permite letras para el apellido.")
            return self.form_invalid(form)
        else:
            cliente.save()
            return super().form_valid(form)


def detalleCliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    return render(request, "cliente/detalleCliente.html", {"cliente": cliente})


@method_decorator(login_required, name="dispatch")
class altaInsumo(CreateView):
    model = Insumo
    form_class = FormInsumo
    template_name = "insumo/altaInsumo.html"
    success_url = reverse_lazy("gestionInsumos")

    def form_valid(self, form):
        insumo = form.save(commit=False)
        if form.cleaned_data["contenido_neto"] <= 0:
            form.add_error(
                "contenido_neto", "El contenido neto ingresado es incorrecto."
            )
            return self.form_invalid(form)
        elif form.cleaned_data["cantidad"] < 0:
            form.add_error("cantidad", "La cantidad ingresada es incorrecta.")
            return self.form_invalid(form)
        else:
            insumo.save()
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class gestionInsumos(ListView):
    model = Insumo
    template_name = "insumo/gestionInsumos.html"
    context_object_name = "insumos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Insumo.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get("estado", "")
        if estado == "Activos" or not estado:
            queryset = Insumo.habilitados.all()
        elif estado == "No activos":
            queryset = Insumo.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "insumo/insumosList.html", context, request=self.request
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class updateInsumo(UpdateView):
    model = Insumo
    form_class = FormInsumo
    template_name = "insumo/modificarInsumo.html"
    success_url = reverse_lazy("gestionInsumos")

    def get_form_kwargs(self):
        kwargs = super(updateInsumo, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs

    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        insumo = form.save(commit=False)
        if (
            form.cleaned_data["activo"] == False
            and CantInsumoServicio.objects.filter(insumo=insumo).exists()
        ):
            # Logica de si quiere desactivar
            form.add_error(
                "activo",
                "No puedes desactivar insumo, porque esta activo en un Tipo de Servicio.",
            )
            return self.form_invalid(form)
        elif form.cleaned_data["contenido_neto"] <= 0:
            form.add_error(
                "contenido_neto", "El contenido neto ingresado es incorrecto."
            )
            return self.form_invalid(form)
        elif form.cleaned_data["cantidad"] < 0:
            form.add_error("cantidad", "La cantidad ingresada es incorrecta.")
            return self.form_invalid(form)
        else:
            insumo.save()
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class altaTipoServicio(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tipoServicio/altaTipoServicio.html"
    success_url = reverse_lazy("gestionTipoServicio")


@method_decorator(login_required, name="dispatch")
class gestionTipoServicio(ListView):
    model = TipoServicio
    template_name = "tipoServicio/gestionTipoServicio.html"
    context_object_name = "tipoServicios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = TipoServicio.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get("estado", "")
        if estado == "Activos" or not estado:
            queryset = TipoServicio.habilitados.all()
        elif estado == "No activos":
            queryset = TipoServicio.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "tipoServicio/tiposServiciosList.html",
                    context,
                    request=self.request,
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@login_required
def tipoServicioDetalles(request, pk):
    tipo = TipoServicio.objects.get(id=pk)
    insumos_qs = CantInsumoServicio.objects.filter(tipoServicio=pk).select_related("insumo")
    maquinarias_qs = tipo.maquinarias.all()

    listInsumos = [{"insumo": cis.insumo, "cantidad": cis.cantidad} for cis in insumos_qs]
    listMaquinarias = list(maquinarias_qs)

    return render(
        request,
        "tipoServicio/detalleTipoServicio.html",
        {
            "tipo": tipo,
            "insumos": listInsumos,
            "maquinarias": listMaquinarias,
        },
    )



@login_required
def maquinariaDetalles(request, pk):
    maquinaria = Maquinaria.objects.get(id=pk)
    return render(
        request, "maquinaria/detalleMaquinaria.html", {"maquinaria": maquinaria}
    )


@method_decorator(login_required, name="dispatch")
class updateTipoServicio(UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tipoServicio/modificarTipoServicio.html"
    success_url = reverse_lazy("gestionTipoServicio")

    def get_form_kwargs(self):
        kwargs = super(updateTipoServicio, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs

    def form_valid(self, form):
        tiposervicio = form.save(commit=False)
        # Verifica si se intenta desactivar un tipoServicio usado por un servicio en curso
        if (
            form.cleaned_data["activo"] is False
            and CantServicioTipoServicio.objects.filter(
                tipoServicio=tiposervicio,
                servicio__estado=4
            ).exists()
        ):
            form.add_error(
                "activo",
                "No puedes desactivar el tipo de servicio, porque un servicio en curso lo está utilizando.",
            )
            return self.form_invalid(form)
        else:
            tiposervicio.save()
            return super().form_valid(form)

def editar_cant_insumos_servicio(request, pk):
    tipo_servicio = get_object_or_404(TipoServicio, pk=pk)
    insumos_servicio = CantInsumoServicio.objects.filter(tipoServicio=tipo_servicio).select_related('insumo')

    if request.method == "POST":
        errores = {}

        for insumo in insumos_servicio:
            nueva_cantidad = request.POST.get(f"cantidad_{insumo.pk}")
            try:
                cantidad_int = int(nueva_cantidad)
                if cantidad_int < 1:
                    errores[f"cantidad_{insumo.pk}"] = f"La cantidad para '{insumo.insumo.descripcion}' debe ser mayor o igual a 1."
                else:
                    insumo.cantidad = cantidad_int
                    insumo.save()
            except (TypeError, ValueError):
                errores[f"cantidad_{insumo.pk}"] = f"Cantidad inválida para '{insumo.insumo.descripcion}'."

        if errores:
            return JsonResponse({"success": False, "errores": errores}, status=400)

        return JsonResponse({"success": True})

    # Esto es lo que se ejecuta en GET para mostrar el modal
    return render(request, 'tipoServicio/editarCantInsumos.html', {
        'tipo_servicio': tipo_servicio,
        'insumos_servicio': insumos_servicio
    })



@method_decorator(login_required, name="dispatch")
class altaMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = "maquinaria/altaMaquinaria.html"
    success_url = reverse_lazy("gestionMaquinaria")


@method_decorator(login_required, name="dispatch")
class gestionMaquinaria(ListView):
    model = Maquinaria
    template_name = "maquinaria/gestionMaquinaria.html"
    context_object_name = "maquinarias"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Maquinaria.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get("estado", "")
        if estado == "Activos" or not estado:
            queryset = Maquinaria.habilitadas.all()
        elif estado == "No activos":
            queryset = Maquinaria.deshabilitadas.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "maquinaria/maquinariasList.html", context, request=self.request
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class updateMaquinaria(UpdateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = "maquinaria/modificarMaquinaria.html"
    success_url = reverse_lazy("gestionMaquinaria")

    def get_form_kwargs(self):
        kwargs = super(updateMaquinaria, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs

    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        maquinaria = form.save(commit=False)
        tipos_servicio_asociados = TipoServicio.habilitados.filter(
            maquinaria=maquinaria
        )
        if form.cleaned_data["activo"] == False and len(tipos_servicio_asociados) > 0:
            # Logica de si quiere desactivar
            form.add_error(
                "activo",
                "No puedes desactivar maquinaria, porque esta activa en un Tipo de Servicio.",
            )
            return self.form_invalid(form)
        else:
            maquinaria.save()
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class altaLocalidad(CreateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = "localidad/altaLocalidad.html"
    success_url = reverse_lazy("gestionLocalidad")


@method_decorator(login_required, name="dispatch")
class updateLocalidad(UpdateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = "localidad/modificarLocalidad.html"
    success_url = reverse_lazy("gestionLocalidad")

    def get_form_kwargs(self):
        kwargs = super(updateLocalidad, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs


@method_decorator(login_required, name="dispatch")
class gestionLocalidad(ListView):
    model = Localidad
    template_name = "localidad/gestionLocalidad.html"
    context_object_name = "localidades"

    def get_queryset(self):
        # Búsqueda dinámica por nombre o CP
        search = self.request.GET.get("search", "")
        if search:
            return Localidad.objects.filter(
                nombre__icontains=search
            ) | Localidad.objects.filter(cp__icontains=search)
        return Localidad.objects.all()

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "localidad/localidadesList.html", context, request=self.request
            )
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class altaEmpleado(CreateView):
    model = Empleado
    form_class = FormEmpleado
    template_name = "empleado/altaEmpleado.html"
    success_url = reverse_lazy("gestionEmpleado")

    def form_valid(self, form):
        empleado = form.save(commit=False)

        if form.cleaned_data["sueldo"] <= 0:
            form.add_error("sueldo", "El sueldo ingresado es incorrecto.")
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data["nombre"]):
            form.add_error("nombre", "Solo se permite letras para el nombre.")
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data["apellido"]):
            form.add_error("apellido", "Solo se permite letras para el apellido.")
            return self.form_invalid(form)
        else:
            # Crear usuario automáticamente
            password = get_random_string(10)
            user = User.objects.create_user(
                username=empleado.email,
                email=empleado.email,
                password=password,
                first_name=empleado.nombre,
                last_name=empleado.apellido,
            )
            grupo_empleado = Group.objects.get(name='Empleado')
            user.groups.add(grupo_empleado)
            empleado.usuario = user
            empleado.save()

            subject = 'Bienvenido a SendaRC - Tus credenciales de acceso'
            from_email = 'SendaRC <sendarccontacto@gmail.com>'
            to = [empleado.email]

            # Texto de respaldo
            text_content = f'''
            Hola {empleado.nombre},

            Tu usuario ha sido creado correctamente.

            Usuario: {empleado.email}
            Contraseña: {password}

            Accedé al sistema en: https://sendarc.onrender.com/

            ¡Bienvenido al equipo!
            '''

            # HTML
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 8px; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                <h2 style="color: #007bff;">¡Bienvenido a SendaRC, {empleado.nombre}!</h2>
                <p>Tu cuenta fue creada correctamente. A continuación te compartimos tus credenciales de acceso:</p>
                <ul>
                    <li><strong>Usuario:</strong> {empleado.email}</li>
                    <li><strong>Contraseña:</strong> {password}</li>
                </ul>
                <p>Podés ingresar al sistema desde el siguiente enlace:</p>
                <p><a href="https://sendarc.onrender.com/" style="background-color: #007bff; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none;">Ingresar al sistema</a></p>
                <hr>
                <p style="font-size: 12px; color: #6c757d;">Este correo fue generado automáticamente. Por favor, no respondas al mismo.</p>
                </div>
            </body>
            </html>
            '''

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return super().form_valid(form)



@method_decorator(login_required, name="dispatch")
class updateEmpleado(UpdateView):
    model = Empleado
    form_class = FormEmpleado
    template_name = "empleado/modificarEmpleado.html"
    success_url = reverse_lazy("gestionEmpleado")

    def get_form_kwargs(self):
        kwargs = super(updateEmpleado, self).get_form_kwargs()
        kwargs["is_modificar"] = True
        return kwargs

    def form_valid(self, form):
        empleado = form.save(commit=False)

        # Verificar si está activo en algún servicio
        frecuencias_empleado = Frecuencia.objects.filter(empleados=empleado)
        activo = any(
            Servicio.objects.get(pk=f.servicio.pk).fecha_finaliza >= timezone.now().date()
            for f in frecuencias_empleado
        )

        if not form.cleaned_data["activo"] and activo:
            form.add_error("activo", "No puedes dar de baja al empleado, porque está activo en un servicio.")
            return self.form_invalid(form)

        if form.cleaned_data["sueldo"] <= 0:
            form.add_error("sueldo", "El sueldo ingresado es incorrecto.")
            return self.form_invalid(form)

        if not re.match("^[A-Za-z]+$", form.cleaned_data["nombre"]):
            form.add_error("nombre", "Solo se permiten letras para el nombre.")
            return self.form_invalid(form)

        if not re.match("^[A-Za-z]+$", form.cleaned_data["apellido"]):
            form.add_error("apellido", "Solo se permiten letras para el apellido.")
            return self.form_invalid(form)

        # Verificar si se cambió el email (username)
        if form.cleaned_data["email"] != empleado.usuario.email:
            # Eliminar el usuario anterior si querés:
            if empleado.usuario:
                empleado.usuario.delete()

            # Crear nuevo usuario
            password = get_random_string(10)
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=password,
                first_name=form.cleaned_data["nombre"],
                last_name=form.cleaned_data["apellido"],
            )
            grupo_empleado = Group.objects.get(name="Empleado")
            user.groups.add(grupo_empleado)
            empleado.usuario = user

            # Enviar email con credenciales nuevas
            subject = '🆕 Tus nuevas credenciales - SendaRC'
            from_email = 'SendaRC <sendarccontacto@gmail.com>'
            to = [user.email]

            text_content = f'''
    Hola {user.first_name},

    Se actualizó tu dirección de correo en el sistema y se ha generado un nuevo acceso.

    Usuario: {user.email}
    Contraseña: {password}

    Ingresá al sistema: https://sendarc.onrender.com/

    Por seguridad, se desactivó tu cuenta anterior.
    '''

            html_content = f'''
    <html><body>
    <h3>Hola {user.first_name},</h3>
    <p>Se actualizó tu dirección de correo en el sistema y se ha generado un nuevo acceso:</p>
    <ul>
    <li><strong>Usuario:</strong> {user.email}</li>
    <li><strong>Contraseña:</strong> {password}</li>
    </ul>
    <p><a href="https://sendarc.onrender.com" style="background:#007bff;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Ingresar al sistema</a></p>
    <p style="font-size:12px;color:#888">Recomendamos cambiar la contraseña al primer ingreso.</p>
    </body></html>
    '''

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        empleado.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class gestionEmpleado(ListView):
    model = Empleado
    template_name = "empleado/gestionEmpleados.html"
    context_object_name = "empleados"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Empleado.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get("estado", "")
        if estado == "Activos" or not estado:
            queryset = Empleado.habilitados.all()
        elif estado == "No activos":
            queryset = Empleado.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "empleado/empleadosList.html", context, request=self.request
                )
                return JsonResponse({"html": html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)


@login_required
def detalleEmpleado(request, pk):
    empleado = Empleado.objects.get(id=pk)
    return render(request, "empleado/detalleEmpleado.html", {"empleado": empleado})

import logging

# Configurar logging
logger = logging.getLogger(__name__)

@login_required
def calendario(request):
    # Obtener el empleado logueado
    try:
        empleado = request.user.empleado
    except AttributeError:
        empleado = None
        logger.warning(f"Usuario {request.user} no tiene empleado asociado")
    
    context = {
        'empleado': empleado,
        'msg': "Calendario de frecuencias asignadas"
    }
    return render(request, "empleado/calendario.html", context)

@login_required
def eventos_calendario(request):
    """Vista AJAX para obtener los eventos del calendario"""
    
    # Verificar que sea una petición AJAX
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Esta vista solo acepta peticiones AJAX'}, status=400)
    
    try:
        # Verificar si el usuario tiene empleado asociado
        if not hasattr(request.user, 'empleado'):
            logger.error(f"Usuario {request.user} no tiene empleado asociado")
            return JsonResponse([], safe=False)
        
        empleado = request.user.empleado
        logger.info(f"Cargando calendario para empleado: {empleado}")
        
        # Obtener frecuencias solo de servicios activos/contratados
        frecuencias = empleado.frecuencias.filter(
            servicio__estado__in=[3, 4]  # Solo servicios contratados o en curso
        ).select_related('servicio')
        
        logger.info(f"Frecuencias encontradas: {frecuencias.count()}")
        
        if frecuencias.count() == 0:
            return JsonResponse([], safe=False)
        
        eventos = []
        
        # Obtener rango de fechas para mostrar en el calendario (ej: próximos 3 meses)
        fecha_vista_inicio = timezone.now().date()
        fecha_vista_fin = fecha_vista_inicio + timedelta(days=90)  # 3 meses
        
        logger.info(f"Rango de vista del calendario: {fecha_vista_inicio} hasta {fecha_vista_fin}")
        
        for frecuencia in frecuencias:
            try:
                # Verificar que la frecuencia tenga servicio
                if not frecuencia.servicio:
                    logger.warning(f"Frecuencia {frecuencia.id} no tiene servicio asociado")
                    continue
                
                servicio = frecuencia.servicio
                
                # Determinar el rango real del servicio
                fecha_inicio_servicio = servicio.fecha_inicio
                fecha_fin_servicio = servicio.fecha_finaliza
                
                # Validar fechas del servicio
                if not fecha_inicio_servicio:
                    logger.warning(f"Servicio {servicio.id} no tiene fecha de inicio")
                    continue
                
                # Si no hay fecha de finalización, usar la fecha de vista máxima
                if not fecha_fin_servicio:
                    # Para servicios sin fecha de fin, mostrar hasta el límite de la vista
                    fecha_fin_servicio = fecha_vista_fin
                    logger.info(f"Servicio {servicio.id} sin fecha fin, usando fecha límite de vista")
                
                # Calcular el rango efectivo (intersección entre servicio y vista)
                fecha_inicio_efectiva = max(fecha_inicio_servicio, fecha_vista_inicio)
                fecha_fin_efectiva = min(fecha_fin_servicio, fecha_vista_fin)
                
                # Si el rango efectivo es válido, calcular las frecuencias
                if fecha_inicio_efectiva <= fecha_fin_efectiva:
                    logger.info(f"Servicio {servicio.id}: Rango efectivo {fecha_inicio_efectiva} - {fecha_fin_efectiva}")
                    
                    # Calcular todas las fechas para esta frecuencia en el rango del servicio
                    fechas_frecuencia = calcular_fechas_frecuencia_por_servicio(
                        frecuencia, fecha_inicio_efectiva, fecha_fin_efectiva
                    )
                    
                    logger.info(f"Frecuencia {frecuencia.id}: {len(fechas_frecuencia)} eventos generados")
                    
                    for fecha in fechas_frecuencia:
                        try:
                            # Verificar que la fecha esté dentro del rango del servicio
                            if not (fecha_inicio_servicio <= fecha <= (fecha_fin_servicio or fecha_vista_fin)):
                                continue
                            
                            # Crear datetime combinando fecha con horarios
                            hora_inicio_dt = frecuencia.getHoraInicio()
                            hora_fin_dt = frecuencia.getHoraFin()
                            
                            if not hora_inicio_dt or not hora_fin_dt:
                                logger.warning(f"Frecuencia {frecuencia.id} no tiene horarios definidos")
                                continue
                            
                            hora_inicio = hora_inicio_dt.time()
                            hora_fin = hora_fin_dt.time()
                            
                            inicio = datetime.combine(fecha, hora_inicio)
                            fin = datetime.combine(fecha, hora_fin)
                            
                            # Crear evento con información completa del servicio
                            evento = {
                                'id': f"freq_{frecuencia.id}_{fecha.strftime('%Y%m%d')}",
                                'title': f"{str(servicio.cliente)} - {frecuencia.getTurno()}",
                                'start': inicio.strftime('%Y-%m-%dT%H:%M:%S'),
                                'end': fin.strftime('%Y-%m-%dT%H:%M:%S'),
                                'backgroundColor': obtener_color_por_turno(frecuencia.turno),
                                'borderColor': obtener_color_por_turno(frecuencia.turno),
                                'textColor': '#ffffff',
                                'extendedProps': {
                                    'servicio_id': servicio.id,
                                    'direccion': str(servicio.direccion or ''),
                                    'cliente': str(servicio.cliente),
                                    'turno': str(frecuencia.getTurno()),
                                    'dia': str(frecuencia.getDia()),
                                    'estado': str(servicio.getEstado()),
                                    'tipo': str(servicio.getTipo()),
                                    'metros2': int(servicio.metros2 or 0),
                                    'fecha_inicio_servicio': servicio.fecha_inicio.strftime('%Y-%m-%d') if servicio.fecha_inicio else '',
                                    'fecha_fin_servicio': servicio.fecha_finaliza.strftime('%Y-%m-%d') if servicio.fecha_finaliza else 'Sin fecha fin',
                                    'duracion_servicio': calcular_duracion_servicio(servicio),
                                }
                            }
                            eventos.append(evento)
                            
                        except Exception as e:
                            logger.error(f"Error procesando fecha {fecha} para frecuencia {frecuencia.id}: {str(e)}")
                            continue
                else:
                    logger.info(f"Servicio {servicio.id}: Sin overlap con rango de vista")
                        
            except Exception as e:
                logger.error(f"Error procesando frecuencia {frecuencia.id}: {str(e)}")
                continue
        
        logger.info(f"Total eventos generados: {len(eventos)}")
        
        # Asegurar que retornamos JSON válido
        return JsonResponse(eventos, safe=False, json_dumps_params={'ensure_ascii': False})
        
    except Exception as e:
        logger.error(f"Error general en eventos_calendario: {str(e)}")
        # En caso de error, retornar array vacío para que el calendario funcione
        return JsonResponse([], safe=False)


def calcular_fechas_frecuencia_por_servicio(frecuencia, fecha_inicio, fecha_fin):
    """
    Calcula todas las fechas en las que se debe realizar una frecuencia
    dentro del rango de duración del servicio
    """
    fechas = []
    
    try:
        # Mapeo de días (1=Lunes, 2=Martes, etc.) a weekday de Python (0=Lunes)
        dia_python = frecuencia.dia - 1
        
        # Encontrar la primera fecha que coincida con el día de la semana
        # dentro del rango del servicio
        fecha_actual = fecha_inicio
        
        # Buscar el primer día de la semana correspondiente
        while fecha_actual <= fecha_fin:
            if fecha_actual.weekday() == dia_python:
                break
            fecha_actual += timedelta(days=1)
        
        # Generar todas las fechas semanales dentro del rango del servicio
        while fecha_actual <= fecha_fin:
            fechas.append(fecha_actual)
            fecha_actual += timedelta(weeks=1)  # Próxima semana
        
        logger.info(f"Frecuencia {frecuencia.id} - Día {frecuencia.getDia()}: {len(fechas)} fechas calculadas")
        
    except Exception as e:
        logger.error(f"Error calculando fechas para frecuencia {frecuencia.id}: {str(e)}")
    
    return fechas


def calcular_duracion_servicio(servicio):
    """Calcula y formatea la duración del servicio"""
    try:
        if not servicio.fecha_inicio:
            return "Sin fecha de inicio"
        
        if not servicio.fecha_finaliza:
            return "Sin fecha de finalización"
        
        duracion = servicio.fecha_finaliza - servicio.fecha_inicio
        dias = duracion.days
        
        if dias == 0:
            return "1 día"
        elif dias < 30:
            return f"{dias} días"
        elif dias < 365:
            meses = dias // 30
            dias_restantes = dias % 30
            if dias_restantes == 0:
                return f"{meses} {'mes' if meses == 1 else 'meses'}"
            else:
                return f"{meses} {'mes' if meses == 1 else 'meses'} y {dias_restantes} días"
        else:
            años = dias // 365
            dias_restantes = dias % 365
            if dias_restantes == 0:
                return f"{años} {'año' if años == 1 else 'años'}"
            else:
                meses_restantes = dias_restantes // 30
                if meses_restantes == 0:
                    return f"{años} {'año' if años == 1 else 'años'} y {dias_restantes} días"
                else:
                    return f"{años} {'año' if años == 1 else 'años'} y {meses_restantes} {'mes' if meses_restantes == 1 else 'meses'}"
    
    except Exception as e:
        logger.error(f"Error calculando duración del servicio {servicio.id}: {str(e)}")
        return "Duración no calculable"


def obtener_color_por_turno(turno):
    """Retorna un color específico según el turno"""
    colores = {
        1: '#28a745',  # Mañana - Verde
        2: '#ffc107',  # Tarde - Amarillo  
        3: '#dc3545',  # Noche - Rojo
    }
    return colores.get(turno, '#6c757d')


@method_decorator(login_required, name='dispatch')
class altaSancion(CreateView):
    model = Sancion
    form_class = FormSancion
    template_name = 'sancion/altaSancion.html'
    success_url = reverse_lazy('gestionSanciones')

@method_decorator(login_required, name='dispatch')
class gestionSancion(ListView):
    model = Sancion
    template_name = 'sancion/gestionSanciones.html'
    context_object_name = 'sanciones'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroSuspensionCorreccionForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = Sancion.objects.select_related('empleado').all()
        estado = self.request.GET.get('estado', '')
        if estado == 'Correccion':
            queryset = queryset.filter(tipo=1)
        elif estado == 'Suspension':
            queryset = queryset.filter(tipo=2)
        
        return queryset.order_by('-fecha_sancion')
    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('sancion/sancionesList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

def detalleSancion(request, pk):
    sancion = Sancion.objects.get(nroSancion=pk)
    return render(request, 'sancion/detalleSancion.html', {'sancion': sancion})



