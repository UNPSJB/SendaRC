from django.shortcuts import render,redirect
from .models import *
from .forms import *
from servicio.models import *
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

class altaCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/altaCliente.html'
    success_url = reverse_lazy('gestionClientes')

    def form_valid(self, form):
        messages.success(self.request, 'El cliente se ha dado de alta correctamente.')
        return super().form_valid(form)

class gestionClientes(ListView):
    model = Cliente
    template_name = 'cliente/gestionClientes.html'
    context_object_name = 'clientes'

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
        messages.success(self.request, 'El cliente se ha modificado correctamente.')
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

class altaMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/altaMaquinaria.html'
    success_url = reverse_lazy('gestionMaquinaria')

class gestionMaquinaria(ListView):
    model = Maquinaria
    template_name = 'maquinaria/gestionMaquinaria.html'
    context_object_name = 'maquinarias' 

class updateMaquinaria(UpdateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/modificarMaquinaria.html'
    success_url = reverse_lazy('gestionMaquinaria')
    def get_form_kwargs(self):
        kwargs = super(updateMaquinaria, self).get_form_kwargs()
        kwargs['is_modificar'] = True  
        return kwargs

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