from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse

# Create your views here.
def gestionClientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/gestionClientes.html', {'clientes': clientes})

def altaCliente(request):
    if request.method == 'GET':
        return render(request, 'cliente/altaCliente.html', {
            'form': ClienteForm()})
    else:
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('gestionClientes')
        
    if '?term' in request.GET:
        qs = Localidad.objects.filter(nombre__icontains=request.GET.get('term'))
        nombres = list()
        for localidad in qs:
            nombres = [localidad.nombre for localidad in qs]
        return JsonResponse(nombres, safe=False)
    return render(request, 'cliente/altaCliente.html', {
        'form': form})

def altaInsumo(request):
    if request.method == 'GET':
        return render(request, 'insumo/altaInsumo.html', {
            'form': FormAltaInsumo()})
    else:
        form = FormAltaInsumo(request.POST)
        if form.is_valid():
            insumo = form.save()
            return redirect('gestionInsumos')
    return render(request, 'insumo/altaInsumo.html', {
        'form': form})

def gestionInsumos(request):
    return render(request, 'insumo/gestionInsumos.html')

def modificarInsumo(request):
    return render(request, 'insumo/modificarInsumo.html')

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
