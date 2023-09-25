from django.shortcuts import render

# Create your views here.
def altaInsumo(request):
    return render(request, 'insumo/altaInsumo.html')

def gestionClientes(request):
    return render (request, 'cliente/gestionClientes.html')

def altaCliente(request):
    return render (request, 'cliente/altaCliente.html')