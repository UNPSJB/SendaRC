import re
from django.shortcuts import render,redirect
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


@method_decorator(login_required, name='dispatch')
class altaCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/altaCliente.html'
    success_url = reverse_lazy('gestionClientes')

    def form_valid(self, form):
        cliente = form.save(commit=False)
        if not re.match("^[A-Za-z]+$", form.cleaned_data['nombre']):
            form.add_error('nombre', 'Solo se permite letras para el nombre.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['apellido']):
            form.add_error('apellido', 'Solo se permite letras para el apellido.')
            return self.form_invalid(form)
        else:
            cliente.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class gestionClientes(ListView):
    model = Cliente
    template_name = 'cliente/gestionClientes.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroClientesForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Cliente.objects.all()
        
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get('estado', '')
        if estado == 'Activos' or not estado:
            queryset = Cliente.habilitados.all()
        elif estado == 'No activos':
            queryset = Cliente.deshabilitados.all()

        # Filtrar por tipo de persona o tipo
        tipo_persona = self.request.GET.get('tipo_persona', '')
        if tipo_persona:
            queryset = queryset.filter(tipoPersona=tipo_persona)

        tipo = self.request.GET.get('tipo', '')
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('cliente/clientesList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)
    
@method_decorator(login_required, name='dispatch')
class updateCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/modificarCliente.html'
    success_url = reverse_lazy('gestionClientes')

    def get_form_kwargs(self):
        kwargs = super(updateCliente, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
    def form_valid(self, form):
        cliente = form.save(commit=False)
        # Verificar si el cliente está asociado a servicios presupuestados, suspendidos, contratados o en curso
        servicios_asociados = Servicio.objects.filter(cliente=cliente, estado__in=[1, 3, 4, 5])
        facturas_asociadas = Factura.objects.filter(cliente=cliente,fechaPago= None)

        
        if form.cleaned_data['activo'] is False and len(servicios_asociados)>0 or len(facturas_asociadas)>0:
            form.add_error('activo', 'Error, el cliente tiene Servicios presupuestados, en curso,suspendidos o Facturas impagas.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['nombre']):
            form.add_error('nombre', 'Solo se permite letras para el nombre.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['apellido']):
            form.add_error('apellido', 'Solo se permite letras para el apellido.')
            return self.form_invalid(form)
        else:
            cliente.save()
            return super().form_valid(form)
def detalleCliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    return render(request, 'cliente/detalleCliente.html', {'cliente': cliente})

@method_decorator(login_required, name='dispatch')
class altaInsumo(CreateView):
    model = Insumo
    form_class = FormInsumo
    template_name = 'insumo/altaInsumo.html'
    success_url = reverse_lazy('gestionInsumos')
    
    def form_valid(self, form):
        insumo = form.save(commit=False)
        if form.cleaned_data['contenido_neto'] <= 0:
            form.add_error('contenido_neto', 'El contenido neto ingresado es incorrecto.')
            return self.form_invalid(form)
        elif form.cleaned_data['cantidad'] <= 0:
            form.add_error('cantidad', 'La cantidad ingresada es incorrecta.')
            return self.form_invalid(form)
        else:
            insumo.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class gestionInsumos(ListView):
    model = Insumo
    template_name = 'insumo/gestionInsumos.html'
    context_object_name = 'insumos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Insumo.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get('estado', '')
        if estado == 'Activos' or not estado:
            queryset = Insumo.habilitados.all()
        elif estado == 'No activos':
            queryset = Insumo.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('insumo/insumosList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@method_decorator(login_required, name='dispatch')
class updateInsumo(UpdateView):
    model = Insumo
    form_class = FormInsumo
    template_name = 'insumo/modificarInsumo.html'
    success_url = reverse_lazy('gestionInsumos')
    def get_form_kwargs(self):
        kwargs = super(updateInsumo, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        insumo = form.save(commit=False)
        if form.cleaned_data['activo'] == False and CantInsumoServicio.objects.filter(insumo=insumo).exists():
            # Logica de si quiere desactivar
            form.add_error('activo', 'No puedes desactivar insumo, porque esta activo en un Tipo de Servicio.')
            return self.form_invalid(form)
        elif form.cleaned_data['contenido_neto'] <= 0:
            form.add_error('contenido_neto', 'El contenido neto ingresado es incorrecto.')
            return self.form_invalid(form)
        elif form.cleaned_data['cantidad'] <= 0:
            form.add_error('cantidad', 'La cantidad ingresada es incorrecta.')
            return self.form_invalid(form)
        else:
            insumo.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class altaTipoServicio(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tipoServicio/altaTipoServicio.html'
    success_url = reverse_lazy('gestionTipoServicio')

@method_decorator(login_required, name='dispatch')
class gestionTipoServicio(ListView):
    model = TipoServicio
    template_name = 'tipoServicio/gestionTipoServicio.html'
    context_object_name = 'tipoServicios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = TipoServicio.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get('estado', '')
        if estado == 'Activos' or not estado:
            queryset = TipoServicio.habilitados.all()
        elif estado == 'No activos':
            queryset = TipoServicio.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('tipoServicio/tiposServiciosList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@login_required
def tipoServicioDetalles(request, pk):
    tipo = TipoServicio.objects.get(id=pk)
    insumos = CantInsumoServicio.objects.filter(tipoServicio=pk)
    maquinarias = TipoServicio.maquinarias.through.objects.filter(tiposervicio_id=pk)
    listInsumos = []
    listMaquinarias = []
    for insumo in insumos:
        listInsumos.append(Insumo.habilitados.get(id=insumo.insumo_id))
    for maquinaria in maquinarias:
        listMaquinarias.append(Maquinaria.objects.get(id=maquinaria.maquinaria_id))
    return render(request, 'tipoServicio/detalleTipoServicio.html', {'tipo': tipo, 'insumos': listInsumos, 'maquinarias': listMaquinarias})

@login_required
def maquinariaDetalles(request, pk):
    maquinaria = Maquinaria.objects.get(id=pk)
    return render(request, 'maquinaria/detalleMaquinaria.html', {'maquinaria': maquinaria})

@method_decorator(login_required, name='dispatch')
class updateTipoServicio(UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tipoServicio/modificarTipoServicio.html'
    success_url = reverse_lazy('gestionTipoServicio')
    def get_form_kwargs(self):
        kwargs = super(updateTipoServicio, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        tiposervicio = form.save(commit=False)
        if form.cleaned_data['activo'] == False and CantServicioTipoServicio.objects.filter(tipoServicio=tiposervicio, servicio=Servicio.estado.en_curso).exists():
            # Logica de si quiere desactivar
            form.add_error('activo', 'No puedes desactivar el tipo de servicio, porque un servicio en curso lo esta utilizando.')
            return self.form_invalid(form)
        else:
            insumo.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class altaMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/altaMaquinaria.html'
    success_url = reverse_lazy('gestionMaquinaria')

@method_decorator(login_required, name='dispatch')
class gestionMaquinaria(ListView):
    model = Maquinaria
    template_name = 'maquinaria/gestionMaquinaria.html'
    context_object_name = 'maquinarias' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Maquinaria.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get('estado', '')
        if estado == 'Activos' or not estado:
            queryset = Maquinaria.habilitadas.all()
        elif estado == 'No activos':
            queryset = Maquinaria.deshabilitadas.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('maquinaria/maquinariasList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@method_decorator(login_required, name='dispatch')
class updateMaquinaria(UpdateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/modificarMaquinaria.html'
    success_url = reverse_lazy('gestionMaquinaria')
    def get_form_kwargs(self):
        kwargs = super(updateMaquinaria, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        maquinaria = form.save(commit=False)
        tipos_servicio_asociados = TipoServicio.habilitados.filter(maquinaria=maquinaria)
        if form.cleaned_data['activo'] == False and len(tipos_servicio_asociados) > 0:
            # Logica de si quiere desactivar
            form.add_error('activo', 'No puedes desactivar maquinaria, porque esta activa en un Tipo de Servicio.')
            return self.form_invalid(form)
        else:
            maquinaria.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class altaLocalidad(CreateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = 'localidad/altaLocalidad.html'
    success_url = reverse_lazy('gestionLocalidad')

@method_decorator(login_required, name='dispatch')    
class updateLocalidad(UpdateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = 'localidad/modificarLocalidad.html'
    success_url = reverse_lazy('gestionLocalidad')
    def get_form_kwargs(self):
        kwargs = super(updateLocalidad, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs

@method_decorator(login_required, name='dispatch')    
class gestionLocalidad(ListView):
    model = Localidad
    template_name = 'localidad/gestionLocalidad.html'
    context_object_name = 'localidades'

@method_decorator(login_required, name='dispatch')    
class altaEmpleado(CreateView):
    model = Empleado
    form_class = FormEmpleado
    template_name = 'empleado/altaEmpleado.html'
    success_url = reverse_lazy('gestionEmpleado')
    
    def form_valid(self, form):
        empleado = form.save(commit=False)
        if form.cleaned_data['sueldo'] <= 0:
            form.add_error('sueldo', 'El sueldo ingresado es incorrecto.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['nombre']):
            form.add_error('nombre', 'Solo se permite letras para el nombre.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['apellido']):
            form.add_error('apellido', 'Solo se permite letras para el apellido.')
            return self.form_invalid(form)
        else:
            empleado.save()
            return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class updateEmpleado(UpdateView):
    model = Empleado
    form_class = FormEmpleado
    template_name = 'empleado/modificarEmpleado.html'
    success_url = reverse_lazy('gestionEmpleado')
    def get_form_kwargs(self):
        kwargs = super(updateEmpleado, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
    def form_valid(self, form):
        # Verifica si el elemento está asociado con OtroModelo
        empleado = form.save(commit=False)
        frecuencias_empleado = Frecuencia.objects.filter(empleados=empleado)
        activo = False
        for frecuencia in frecuencias_empleado:
            servicio_frecuencia = Servicio.objects.get(pk=frecuencia.servicio.pk)
            fecha_actual = timezone.now().date()
            if servicio_frecuencia.fecha_finaliza >= fecha_actual:
                activo = True
                break
            
        if form.cleaned_data['activo'] == False and activo == True:
            # Logica de si quiere desactivar
            form.add_error('activo', 'No puedes dar de baja al empleado, porque esta activo en un servicio.')
            return self.form_invalid(form)
        elif form.cleaned_data['sueldo'] <= 0:
            form.add_error('sueldo', 'El sueldo ingresado es incorrecto.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['nombre']):
            form.add_error('nombre', 'Solo se permite letras para el nombre.')
            return self.form_invalid(form)
        elif not re.match("^[A-Za-z]+$", form.cleaned_data['apellido']):
            form.add_error('apellido', 'Solo se permite letras para el apellido.')
            return self.form_invalid(form)
        else:
            empleado.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class gestionEmpleado(ListView):
    model = Empleado
    template_name = 'empleado/gestionEmpleados.html'  
    context_object_name = 'empleados'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltroActivoForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Empleado.objects.all()
        # Filtrar por estado (activo o no activo)
        estado = self.request.GET.get('estado', '')
        if estado == 'Activos' or not estado:
            queryset = Empleado.habilitados.all()
        elif estado == 'No activos':
            queryset = Empleado.deshabilitados.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('empleado/empleadosList.html', context, request=self.request)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@login_required
def detalleEmpleado(request, pk):
    empleado = Empleado.objects.get(id=pk)
    return render(request, 'empleado/detalleEmpleado.html', {'empleado': empleado})

@method_decorator(login_required, name='dispatch')
class altaSancion(CreateView):
    model = Sancion
    form_class = FormSancion
    template_name = 'sancion/altaSancion.html'
    success_url = reverse_lazy('gestionSanciones')

@method_decorator(login_required, name='dispatch')
class updateSancion(UpdateView):
    model = Sancion
    form_class = FormSancion
    template_name = 'sancion/modificarSancion.html'
    success_url = reverse_lazy('gestionSanciones')
    def get_form_kwargs(self):
        kwargs = super(updateSancion, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs

@method_decorator(login_required, name='dispatch')
class gestionSancion(ListView):
    model = Sancion
    template_name = 'sancion/gestionSanciones.html'
    context_object_name = 'sanciones'

@login_required
def calendario(request):
    mensaje = "hola"
    return render(request, 'calendario/calendario.html',{'msg':mensaje})
    
