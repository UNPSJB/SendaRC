from django.shortcuts import render
from django.forms import *
from .models import Cliente

# Create your views here.
def gestionClientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/gestionClientes.html', {'clientes': clientes})

def altaCliente(request):
    return render (request, 'cliente/altaCliente.html')

def altaInsumo(request):
    return render(request, 'insumo/altaInsumo.html')

def gestionInsumos(request):
    return render(request, 'insumo/gestionInsumos.html')

def modificarInsumo(request):
    return render(request, 'insumo/modificarInsumo.html')

