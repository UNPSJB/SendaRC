from django.shortcuts import render, redirect
from core.models import *
from .forms import *


class PresupuestoSession(dict):
    FIELDS = ["direccion", "metros2", "observaciones", "tipo"]
    FIELDS2 = ["tipoServicio"]
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
        if "listaServicios" in session:
            p.update(session["listaServicios"])
        return p
    
    def store(self):
        data = {k: v for k, v in self.items() if k in self.FIELDS}
        data["cliente_pk"] = self["cliente"].pk
        self.session["presupuesto"] = data
        
    def storeServicio(self):
        data = {k: v for k, v in self.items() if k in self.FIELDS2}
        print(data)
        lista = []
        lista.append(self["tipoServicios"])
        data["listaServicio"] = lista
        self.session["presupuesto"] = data
    
    def storeFrecuencia(self):
        data = {k: v for k, v in self.items() if k in self.FIELDS}
        
        self.session["presupuesto"] = data

    def save():
        pass

    @property
    def cliente(self):
        print("hoa")
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
            p.update(form.cleaned_data)
            p.store()
            return redirect('presupuestarServicios')
    else:
        p = PresupuestoSession.create(request.session)
        form = FormPresupuestoCliente(initial=p)
    return render(request, 'servicio/presupuestarCliente.html', {'form': form, 'presupuesto': p})

def presupuestarServicios(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        form = FormServicios(request.POST)
        if form.is_valid():
            p.update(form.cleaned_data)
            p.storeServicio()
        return redirect('presupuestarConfirmar')
    else:
        form = FormServicios()
    return render(request, 'servicio/presupuestarServicios.html', {'form': form, 'presupuesto': p})

def presupuestarConfirmar(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p.update(form.cleaned_data)
            model = p.save()
            return redirect('presupuestarImprimir', {"pk": model.pk})
    else:
        form = FormPresupuestoCliente()
    return render(request, 'servicio/presupuestarConfirmar.html', {'form': form})

def presupuestarImprimir(request, pk):
    return render(request, 'servicio/presupuestarImprimir.html', {'form': FormPresupuestoCliente})
