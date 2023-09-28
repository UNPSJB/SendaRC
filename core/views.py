from django.shortcuts import render
from django.forms import *

# Create your views here.
def gestionClientes(request):
    return render (request, 'cliente/gestionClientes.html')

def altaCliente(request):
    return render (request, 'cliente/altaCliente.html')

def altaInsumo(request):
    return render(request, 'insumo/altaInsumo.html')

def gestionInsumo(request):
    return render(request, 'insumo/gestionInsumo.html')

def modificarInsumo(request):
    return render(request, 'insumo/modificarInsumo.html')

