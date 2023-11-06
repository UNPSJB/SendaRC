from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from core.models import *
from .forms import *


class PresupuestoSession(dict):
    FIELDS = ["direccion", "metros2", "observaciones", "tipo"]
    # Create init for PresupuestoSession
    def __init__(self, session=None):
        self.session = session

    @classmethod
    def create(cls, session):
        return cls(session)
        
    @classmethod
    def getOrCreate(cls, session):
        p = PresupuestoSession.create(session)
        if "presupuesto" in session:
            p.update(session["presupuesto"])
        return p
    
    @classmethod
    def limpiarSession(cls, session):
        p = PresupuestoSession.create(session)
        
    
    def store(self):
        data = {k: v for k, v in self.items() if k in self.FIELDS} #Empareja y guarda solo los campos del formulario que nos interesa no ?
        data["cliente_pk"] = self["cliente"].pk     # agrega una clave para el pk del cliente 
        self.session["presupuesto"] = data      # almacena todas la claves en la clave presupuesto de la session no ? 
        
    def storeServicio(self):
        data = self.session.get("servicios", [])
        servicio_data = {
            "tipo_servicio": self["tipo_servicio"].pk,
            "cantidad": self["cantidad"],
        }
        data.append(servicio_data)
        self.session["servicios"] = data
    
    def storeFrecuencia(self):
        data = self.session.get("frecuencias", [])
        frecuencia_data = {
            "dia": self["dia"],
            "turno": self["turno"],
        }
        data.append(frecuencia_data)
        self.session["frecuencias"] = data

    def save():
        pass

    @property
    def cliente(self):
        if "cliente" not in self:
            self["cliente"] = Cliente.objects.get(pk=self["cliente_pk"])
        return self["cliente"]
    
# Create your views here.
def gestionServicios(request):
    return render(request, 'servicio/gestionServicios.html')

def presupuestarCliente(request):
    if (request.method == 'POST'):
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p = PresupuestoSession.getOrCreate(request.session)
            p.update(form.cleaned_data)     # Se guarda todos los campos y sus valores del formularios en p ?
            p.store()
            return redirect('presupuestarServicios')
    else:
        request.session['presupuesto'] = {}
        request.session['servicios'] = []
        request.session['frecuencias'] = []
        p = PresupuestoSession.create(request.session)
        form = FormPresupuestoCliente(initial=p)
        print("-------Estoy en GET Presupuestar Cliente-- Valido session vacia")
        print(p.session["presupuesto"])
    return render(request, 'servicio/presupuestarCliente.html', {'form': form, 'presupuesto': p})

def presupuestarServicios(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        formset = formset_factory(FormBaseTipoServicio, extra=1)
        formset = formset(request.POST)
        if formset.is_valid():
            for f in formset:
                #cleaned_data = f.cleaned_data
                p.update(f.cleaned_data)
                p.storeServicio()
                print("-------Estoy en POST Presupuestar Servicio")
                print(p.session["servicios"])
            return redirect('presupuestarFrecuencias')
        else :
            print(formset.errors)
    else:
        formset = formset_factory(FormBaseTipoServicio, extra=1)
        if "servicios" in p.session["servicios"]:
            formset = formset(initial=p.session["servicios"])
        print("-------Estoy en GET Presupuestar Servicios")
        print(p.session["presupuesto"])
    return render(request, 'servicio/presupuestarServicios.html', {'formset': formset, 'presupuesto': p})

def presupuestarFrecuencias(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        formset = formset_factory(FormBaseFrecuencia, extra=1)
        formset = formset(request.POST)
        if formset.is_valid():
            for f in formset:
                #cleaned_data = f.cleaned_data
                p.update(f.cleaned_data)
                p.storeFrecuencia()
                print("-------Estoy en POST Presupuestar Frecuencia")
                print(p.session["servicios"])
            return redirect('presupuestarConfirmar')
        else :
            print(formset.errors)
    else:
        formset = formset_factory(FormBaseFrecuencia, extra=1)
        # Accede a todos los elementos guardados en la lista 'servicios' en la sesión
        servicios_guardados = p.session["servicios"]
        if "frecuencias" in p.session["frecuencias"]:
            formset = formset(initial=p.session["frecuencias"])
        print("----------------Estoy en GET Presupuestar Frecuencias ")
        print(servicios_guardados)
    return render(request, 'servicio/presupuestarFrecuencia.html', {'formset': formset, 'presupuesto': p, 'tipo_Servicios': servicios_guardados})

def presupuestarConfirmar(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        form = FormConfirmar(request.POST)
        if form.is_valid():
            print("-------Estoy en POST Presupuestar Confirmar")
            p.update(form.cleaned_data)
            model = p.save()
            return redirect('presupuestarImprimir', {"pk": model.pk})
    else:
        form = FormConfirmar()
        servicios_guardados = p.session["servicios"]
        frecuencias_guardadas = p.session["frecuencias"]
        print("-------Estoy en GET Presupuestar Confirmar")
        print(p.session["servicios"])
        print(p.session["frecuencias"])
    return render(request, 'servicio/presupuestarConfirmar.html', {'form': form, 'presupuesto': p, 'tipo_Servicios': servicios_guardados, 'frecuencias': frecuencias_guardadas})

def presupuestarImprimir(request, pk):
    return render(request, 'servicio/presupuestarImprimir.html', {'form': FormPresupuestoCliente})
