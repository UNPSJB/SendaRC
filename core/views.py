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
            queryset = queryset.filter(activo=True)
        elif estado == 'No activos':
            queryset = queryset.filter(activo=False)

        # Filtrar por tipo de persona o tipo
        tipo_persona = self.request.GET.get('tipo_persona', '')
        if tipo_persona:
            queryset = queryset.filter(tipoPersona=tipo_persona)

        tipo = self.request.GET.get('tipo', '')
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset
    

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
        facturas_asociadas = Factura.objects.filter(cliente=cliente,fechaPago=None)

        
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

class altaInsumo(CreateView):
    model = Insumo
    form_class = FormInsumo
    template_name = 'insumo/altaInsumo.html'
    success_url = reverse_lazy('gestionInsumos')

class gestionInsumos(ListView):
    model = Insumo
    template_name = 'insumo/gestionInsumos.html'
    context_object_name = 'insumos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ['Habilitado', 'Deshabilitado', 'Todos']
        
        estado = self.request.GET.get('estado', '')
        if estado == 'Habilitado' or not estado:
            context['insumos'] = Insumo.habilitados.all()
        elif estado == 'Deshabilitado':
            context['insumos'] = Insumo.deshabilitados.all()
        elif estado == 'Todos':
            context['insumos'] = Insumo.objects.all()
        return context

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
        else:
            insumo.save()
            return super().form_valid(form)

class altaTipoServicio(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tipoServicio/altaTipoServicio.html'
    success_url = reverse_lazy('gestionTipoServicio')

class gestionTipoServicio(ListView):
    model = TipoServicio
    template_name = 'tipoServicio/gestionTipoServicio.html'
    context_object_name = 'tipoServicios'

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

def maquinariaDetalles(request, pk):
    maquinaria = Maquinaria.objects.get(id=pk)
    return render(request, 'maquinaria/detalleMaquinaria.html', {'maquinaria': maquinaria})

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

class altaMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/altaMaquinaria.html'
    success_url = reverse_lazy('gestionMaquinaria')

class gestionMaquinaria(ListView):
    model = Maquinaria
    template_name = 'maquinaria/gestionMaquinaria.html'
    context_object_name = 'maquinarias' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ['Activas', 'No activas', 'Todas']
        
        estado = self.request.GET.get('estado', '')
        if estado == 'Activas' or not estado:
            context['maquinarias'] = Maquinaria.habilitadas.all()
        elif estado == 'No activas':
            context['maquinarias'] = Maquinaria.deshabilitadas.all()
        elif estado == 'Todas':
            context['maquinarias'] = Maquinaria.objects.all()
        return context

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

class altaLocalidad(CreateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = 'localidad/altaLocalidad.html'
    success_url = reverse_lazy('gestionLocalidad')
    
class updateLocalidad(UpdateView):
    model = Localidad
    form_class = FormLocalidad
    template_name = 'localidad/modificarLocalidad.html'
    success_url = reverse_lazy('gestionLocalidad')
    def get_form_kwargs(self):
        kwargs = super(updateLocalidad, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
class gestionLocalidad(ListView):
    model = Localidad
    template_name = 'localidad/gestionLocalidad.html'
    context_object_name = 'localidades'
    
class altaEmpleado(CreateView):
    model = Empleado
    form_class = FormEmpleado
    template_name = 'empleado/altaEmpleado.html'
    success_url = reverse_lazy('gestionEmpleado')
    
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
        else:
            empleado.save()
            return super().form_valid(form)

class gestionEmpleado(ListView):
    model = Empleado
    template_name = 'empleado/gestionEmpleados.html'  
    context_object_name = 'empleados'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ['Habilitado', 'Deshabilitado', 'Todos']
        
        estado = self.request.GET.get('estado', '')
        if estado == 'Habilitado' or not estado:
            context['empleados'] = Empleado.habilitados.all()
        elif estado == 'Deshabilitado':
            context['empleados'] = Empleado.deshabilitados.all()
        elif estado == 'Todos':
            context['empleados'] = Empleado.objects.all()
        return context
def detalleEmpleado(request, pk):
    empleado = Empleado.objects.get(id=pk)
    return render(request, 'empleado/detalleEmpleado.html', {'empleado': empleado})

class altaSancion(CreateView):
    model = Sancion
    form_class = FormSancion
    template_name = 'sancion/altaSancion.html'
    success_url = reverse_lazy('gestionSanciones')
    
class updateSancion(UpdateView):
    model = Sancion
    form_class = FormSancion
    template_name = 'sancion/modificarSancion.html'
    success_url = reverse_lazy('gestionSanciones')
    def get_form_kwargs(self):
        kwargs = super(updateSancion, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs
    
class gestionSancion(ListView):
    model = Sancion
    template_name = 'sancion/gestionSanciones.html'
    context_object_name = 'sanciones'
    
