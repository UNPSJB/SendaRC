from django.shortcuts import render, redirect
from django.views.generic import CreateView

from datetime import datetime

from .forms import *
from .models import *


# Create your views here.

def crearFacturaSeña(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    cliente = servicio.cliente
    factura_seña = Factura.objects.create(servicio=servicio, 
        importe=servicio.importe_total*0.50, 
        cliente=cliente,
        tipo=1,
        fechaEmision=datetime.now())
    factura_seña.save()
    return redirect(to='detallesFacturaSeña', pk=factura_seña.pk)

def detallesFacturaSeña(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    return render(request, 'factura/detallesFacturaSeña.html', {'factura_seña':factura_seña})

def realizarCobroFacturaSeña(request, pk):
    if request.method == 'POST':
        factura_seña = Factura.objects.get(pk=pk)
        form = FormCobroFacturaSeña(request.POST)
        if form.is_valid():
            factura_seña.formaPago = form.cleaned_data['formapago']
            factura_seña.fechaPago = datetime.now()
            factura_seña.save()            
            servicio = Servicio.objects.get(pk=factura_seña.servicio.pk)
            servicio.estado = 3
            servicio.save()
            return redirect('facturaPagada', pk=factura_seña.pk)
        else:
            print(form.errors)
        return render(request, '')
    facturaSeña = Factura.objects.get(pk=pk)
    servicio = facturaSeña.servicio
    form = FormCobroFacturaSeña()
    context = {
        'servicio': servicio,
        'facturaSeña':facturaSeña,
        'form': form
    }
    return render(request, 'factura/CobroFacturaSeña.html', context)

def facturaPagada(request, pk):
    factura_seña = Factura.objects.get(pk=pk)
    context = {
        'factura_seña':factura_seña
    }
    return render(request, 'factura/facturaSeñaPagada.html', context)