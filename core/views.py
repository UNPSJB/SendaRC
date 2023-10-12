from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

# Create your views here.
def gestionClientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/gestionClientes.html', {'clientes': clientes})

def altaCliente(request):
    if request.method == 'GET':
        localidades = Localidad.objects.all()
        return render(request, 'cliente/altaCliente.html', {
            'form': ClienteForm(),
            'localidadesList':localidades
        })
    else:
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('gestionClientes')
    
    return render(request, 'cliente/altaCliente.html', {
        'form': form})

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
