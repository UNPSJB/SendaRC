from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

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

class altaInsumo(CreateView):
    model = Insumo
    form_class = FormAltaInsumo
    template_name = 'insumo/altaInsumo.html'
    success_url = reverse_lazy('gestionInsumos')

class gestionInsumos(ListView):
    model = Insumo
    template_name = 'insumo/gestionInsumos.html'
    context_object_name = 'insumos'

class updateInsumo(UpdateView):
    model = Insumo
    form_class = FormModificarInsumo
    template_name = 'insumo/modificarInsumo.html'
    success_url = reverse_lazy('gestionInsumos')

def altaTipoServicio(request):
    if request.method == 'GET':
        return render(request, 'tipoServicio/altaTipoServicio.html', {
            'form': TipoServicioForm()})
    else:
        form = FormAltaTipoServicio(request.POST)
        if form.is_valid():
            tipoServicio = form.save()
            return redirect('gestionTipoServicio', {
                'tipoServicio': tipoServicio})

def gestionTipoServicio(request):
    return render(request, 'tipoServicio/gestionTipoServicio.html', {
        'tipoServicios': TipoServicio.objects.all()
    })


class altaMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormAltaMaquinaria
    template_name = 'maquinaria/altaMaquinaria.html'


    

