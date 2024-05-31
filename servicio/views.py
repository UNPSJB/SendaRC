from typing import Any, Self
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django import forms
from core.models import *
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string


def calcularPorcentaje(total_importe, porcentaje):
    cambio = (porcentaje / 100) * total_importe
    total_importe = total_importe + cambio
    return total_importe

def calcularImportePresupuesto(listaTipoServicio, cantEmpleados, cantFrecuencias, tipo):
    importe_sugerido = 0
    dicc_total_importe = {}
    tipos_servicios_precios = 0
    for tipo in listaTipoServicio:
        tipos_servicios_precios += tipo['tipo_servicio'].getPrecio(tipo['cantidad']) #Su suma el precio de cada tipoServicio por su cantidad
    #El total de los servicios que se hacen todos los turnos
    total_servicios = tipos_servicios_precios * cantFrecuencias
    dicc_total_importe['total_servicios'] = total_servicios = tipos_servicios_precios * cantFrecuencias
    #Calculamos la cantidad de empleados real que vamos a necesitar para todo el servicio 
    if tipo == 'Determinado':
        cant_empleados = cantFrecuencias * cantEmpleados *  4      #El 4 es por el mes tiene cuatro semanas
    else:
        cant_empleados = cantFrecuencias * cantEmpleados    #El Eventual puede tener min=1 y max=3, 3 siempre y cuando sean el mismo dia
    mano_obra = Empleado.getSueldoBasico() / 24     #Empleados trabajan solo un turno por dia, por lo tanto los posibles dias de trabajo son 24
    #La cantidad de empleados damos a entender que es la estimativa por turno
    importe_sugerido = 1.15 * total_servicios + (mano_obra * cant_empleados)   #El 1.15 representa el costo mas el 15% de ganancias 
    dicc_total_importe['porcentaje_ganancia'] = (15 / 100) * total_servicios
    dicc_total_importe['mano_obra_servicio'] = mano_obra * cant_empleados
    dicc_total_importe['importe_sugerido'] = importe_sugerido
    return dicc_total_importe

def saveServicio(datos_cliente, form_data, total, servicio_pk):
    new_servicio = None
    if servicio_pk == None:
        new_servicio = Servicio(plazo_vigencia=timezone.now() + timedelta(days=10),
                                cliente=Cliente.objects.get(pk=datos_cliente['cliente_pk']),
                                direccion=datos_cliente['direccion'],
                                metros2=datos_cliente['metros2'],
                                observaciones=datos_cliente['observaciones'],
                                cant_empleados=form_data['cantidad_empleados'],
                                porcentaje=form_data['porcentaje'],
                                tipo=datos_cliente['tipo'],
                                estado=1,
                                importe_total=total)
        new_servicio.save()
    else:
        print("-------ELSE PARA MODIFICAR ")
        new_servicio = Servicio.objects.get(pk=servicio_pk)
        new_servicio.cliente = Cliente.objects.get(pk=datos_cliente['cliente_pk'])
        new_servicio.direccion = datos_cliente['direccion']
        new_servicio.metros2 = datos_cliente['metros2']
        new_servicio.observaciones = datos_cliente['observaciones']
        new_servicio.cant_empleados = form_data['cantidad_empleados']
        new_servicio.porcentaje = form_data['porcentaje']
        new_servicio.tipo = datos_cliente['tipo']
        new_servicio.estado = 1
        new_servicio.importe_total= total
        new_servicio.save()
    return new_servicio

def saveTipoServicios(servicio, listTipoServicio, servicio_pk):
    if servicio_pk != None:
        CantServicioTipoServicio.objects.filter(servicio=servicio).delete()
    
    for tipo in listTipoServicio:
        new_servicio_tipo_servicio = CantServicioTipoServicio.objects.create(servicio=servicio,
                                                            tipoServicio= TipoServicio.objects.get(pk=tipo['tipo_servicio'].pk),
                                                            cantidad=tipo['cantidad'])
        
def saveFrecuenca(servicio, listFrecuencias, servicio_pk):
    if servicio_pk != None:
        Frecuencia.objects.filter(servicio=servicio).delete()
        
    for frecuencia in listFrecuencias:
        dia_num = next((key for key, value in Frecuencia.DIA if value == frecuencia['dia']), None)
        turno_num = next((key for key, value in Frecuencia.TURNO if value == frecuencia['turno']), None)
        Frecuencia.objects.create(dia=dia_num, turno=turno_num, servicio=servicio)
        #new_frecuencia = Frecuencia.objects.create(dia=dia_num, turno=turno_num, servicio=servicio)
        
def recargarSession(servicio, presupuestoSession):
    #Cargamos los datos del cliente que ya estaban
    datos_cliente = {'direccion': servicio.direccion,
                     'metros2': servicio.metros2,
                     'observaciones': servicio.observaciones,
                     'tipo': servicio.tipo,
                     'cliente': servicio.cliente}
    presupuestoSession.update(datos_cliente)
    presupuestoSession.store()
    #Cargamos la lista de tipos de servicio del servicio a modificar
    lista_tipos_servicio = CantServicioTipoServicio.objects.filter(servicio=servicio)
    for tipo_servicio in lista_tipos_servicio:
        tipo_servicio_data = {'tipo_servicio': tipo_servicio.tipoServicio,
                              'cantidad': tipo_servicio.cantidad}
        presupuestoSession.update(tipo_servicio_data)
        presupuestoSession.storeServicio()
    #Cargamos la lista de frecuencias del servicio a modificar
    lista_frecuencias = Frecuencia.objects.filter(servicio=servicio)
    for frecuencia in lista_frecuencias:
        frecuencia_data = {'dia': frecuencia.dia,
                           'turno': frecuencia.turno}
        presupuestoSession.update(frecuencia_data)
        presupuestoSession.storeFrecuencia()
    #Debemos devolver el presupuestoSession ? creo que no
    #return presupuestoSession


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
    def getTipoServicio(cls, session):
        listaS = []
        if "servicios" in session:
            listaS = session["servicios"]
        for item in listaS:
            item['tipo_servicio'] = TipoServicio.objects.get(pk=item['tipo_servicio'])
        return listaS
    
    @classmethod
    def getFrecuencia(cls, session):
        listaF = []    
        MAP_DIA = dict(Frecuencia.DIA)
        MAP_TURNO = dict(Frecuencia.TURNO)
        if "frecuencias" in session:
            listaF = session["frecuencias"]
        for item in listaF:
            dia = int(item['dia'])
            item['dia'] = MAP_DIA.get(dia)
            turno = int(item['turno'])
            item['turno'] = MAP_TURNO.get(turno)
        return listaF
    
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
            
    @property
    def cliente(self):
        if "cliente" not in self:
            self["cliente"] = Cliente.objects.get(pk=self["cliente_pk"])
        return self["cliente"]
    
@method_decorator(login_required, name='dispatch')
class gestionServicios(ListView):
    model = Servicio
    template_name = 'servicio/gestionServicios.html'
    context_object_name = 'servicios'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FiltrosServiciosForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Servicio.objects.all()   
        # Filtrar por estado
        estado_servicio = self.request.GET.get('estado', '')
        tipo_servicio = self.request.GET.get('tipo', '')
        
        if tipo_servicio:
            queryset = queryset.filter(tipo=tipo_servicio)
        if estado_servicio:
            queryset = queryset.filter(estado=estado_servicio)

        # Filtrar por fecha de inicio
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio=fecha_inicio)
            print(queryset)
        # Filtrar por fecha de finalización
        fecha_finaliza = self.request.GET.get('fecha_finaliza', '')
        if fecha_finaliza:
            queryset = queryset.filter(fecha_finaliza=fecha_finaliza)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        self.request.session['presupuesto'] = {}
        self.request.session['servicios'] = []
        self.request.session['frecuencias'] = []
        self.request.session['servicio_pk'] = None
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('servicio/serviciosList.html', context, request=self.request)
                print(html)
                return JsonResponse({'html': html})
            else:
                return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print(f"Error al renderizar la respuesta: {e}")
            return super().render_to_response(context, **response_kwargs)

@login_required
#vista que utiliza en canvas (modal) en la gestion para ver un miniResumen de un servicio
def canvasServicio(request, pk):
    servicio = Servicio.objects.get(id=pk)
    return render(request, 'servicio/canvasServicio.html', {'servicio': servicio})

@login_required
def presupuestarCliente(request, pk=None):
    presupuesto_session = PresupuestoSession.getOrCreate(request.session)
    cliente = None    
    if (request.method == 'POST'):
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p = PresupuestoSession.getOrCreate(request.session)
            p.update(form.cleaned_data)     # Se guarda todos  los campos y sus valores 
            p.store()
            return redirect('presupuestarServicios')
        else:
            print(form.errors)
    else:
        form = FormPresupuestoCliente()
        if pk:
            print("TRAIGO PK A PRESUPUESTAR CLIENTE")
            servicio = Servicio.objects.get(pk=pk)
            recargarSession(servicio, presupuesto_session)
            request.session['servicio_pk'] = pk
        else:
            print("NO TRAIGO PK A PRESUPUESTAR CLIENTE")
            request.session['servicio_pk'] = None
        dicc = request.session.get("presupuesto", {})
        if len(dicc) == 0:
            form = FormPresupuestoCliente()
        else:
            cliente = Cliente.habilitados.get(pk=dicc['cliente_pk'])
            form = FormPresupuestoCliente(initial={'cliente': cliente, 'tipo': dicc['tipo'], 'direccion': dicc['direccion'], 'metros2': dicc['metros2'], 'observaciones': dicc['observaciones']})
            form.fields['cliente'].widget = forms.HiddenInput(attrs={'hidden': True, 'required': False})
        print("-------Estoy en GET Presupuestar Cliente", )
        
    return render(request, 'servicio/presupuestarCliente.html', {'form': form, 'cliente': cliente})

@login_required
def presupuestarIdCliente(request, pk):
    presupuesto_session = PresupuestoSession.getOrCreate(request.session)    
    cliente = Cliente.habilitados.get(pk=pk)
    if (request.method == 'POST'):
        form = FormPresupuestoCliente(request.POST)
        if form.is_valid():
            p = PresupuestoSession.getOrCreate(request.session)
            p.update(form.cleaned_data)     # Se guarda todos  los campos y sus valores 
            p.store()
            return redirect('presupuestarServicios')
        else:
            print(form.errors)
    else:
        dicc = request.session.get("presupuesto", {})
        if len(dicc) == 0:
            form = FormPresupuestoCliente(initial={'cliente': cliente.pk})
            form.fields['cliente'].widget = forms.HiddenInput(attrs={'hidden': True, 'required': False})
        else:
            form = FormPresupuestoCliente(initial=presupuesto_session.session["presupuesto"])
            form.fields['cliente'].widget = forms.HiddenInput(attrs={'hidden': True, 'required': False})
        print("-------Estoy en GET Presupuestar ID Cliente", presupuesto_session.session["presupuesto"])
    return render(request, 'servicio/presupuestarCliente.html', {'form': form, 'cliente': cliente})

@login_required
def presupuestarServicios(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        formset = formset_factory(FormBaseTipoServicio)
        formset = formset(request.POST)
        p.session["servicios"] = []
        if formset.is_valid():
            for f in formset:
                cantidad = f.cleaned_data['cantidad'] 
                
                if cantidad <= 0 or cantidad >= 300:
                    f.add_error('cantidad', 'Los valores ingresados no son validos.')
                    return render(request, 'servicio/presupuestarServicios.html', {'formset': formset, 'presupuesto': p})
                
                p.update(f.cleaned_data)
                p.storeServicio()
                print("-------Estoy en POST Presupuestar Servicio")
                print(p.session["servicios"])
            return redirect('presupuestarFrecuencias')
        else :
            print(formset.errors)
    else:
        lista = request.session.get("servicios", [])
        if len(lista) == 0:
            formset = formset_factory(FormBaseTipoServicio, extra=1)
        else:
            print("COSAS DE LA LISTA EN GET", lista, len(lista))
            formset = formset_factory(FormBaseTipoServicio, extra=0)
            if "servicios" in p.session:
                formset = formset(initial=p.session["servicios"])
        print("-------Estoy en GET Presupuestar Servicios")
        print(p.session["presupuesto"])
    return render(request, 'servicio/presupuestarServicios.html', {'formset': formset, 'presupuesto': p})

@login_required
def presupuestarFrecuencias(request):
    p = PresupuestoSession.getOrCreate(request.session)
    if (request.method == 'POST'):
        formset = formset_factory(FormBaseFrecuencia, extra=1)
        formset = formset(request.POST)
        p.session["frecuencias"] = []    
        dias_turnos = {}
        if formset.is_valid():
            for f in formset:
                dia = f.cleaned_data['dia']
                turno = f.cleaned_data['turno']
                
                if dia not in dias_turnos:
                    dias_turnos[dia] = set()
                
                if dia in dias_turnos and len(dias_turnos[dia]) >= 3:
                    f.add_error('turno', 'Un dia solo puede tener 3 turnos distintos.')
                    return render(request, 'servicio/presupuestarFrecuencia.html', {'formset': formset, 'presupuesto': p})
                
                if dia in dias_turnos and turno in dias_turnos[dia]:
                    f.add_error('turno', 'No se permiten turnos duplicados para el mismo dia')
                    return render(request, 'servicio/presupuestarFrecuencia.html', {'formset': formset, 'presupuesto': p})
                
                dicc = p.session['presupuesto']
                print("--------------QUE TIENE DIA, Y QUE TIENE DIAS_TURNOS Y QUE TIENE LEN(DIAS_TURNOS)", dia, dias_turnos, len(dias_turnos), len(dias_turnos[dia]))
                if dicc['tipo'] == 1 and dia in dias_turnos and len(dias_turnos) > 1:
                    print("--------------QUE TIENE P.SESSION Y QUE TIENE DICC", dicc)
                    f.add_error('turno', 'Servicio eventual, solo 3 frecuencia, mismo dia, y distintos turnos')
                    f.add_error('dia', 'Servicio eventual, solo 3 frecuencia, mismo dia, y distintos turnos')
                    return render(request, 'servicio/presupuestarFrecuencia.html', {'formset': formset, 'presupuesto': p})
                
                
                dias_turnos[dia].add(turno)
                
                p.update(f.cleaned_data)
                p.storeFrecuencia()
                print("-------Estoy en POST Presupuestar Frecuencia")
                print(p.session["servicios"])
            return redirect('presupuestarConfirmar')
        else :
            print(formset.errors)
    else:
        lista = request.session.get("frecuencias", [])
        if len(lista) == 0:
            formset = formset_factory(FormBaseFrecuencia, extra=1)    
            print("COSAS DE LA LISTA EN GET", lista, len(lista))
        else:
            formset = formset_factory(FormBaseFrecuencia, extra=0)
            if "frecuencias" in p.session:
                formset = formset(initial=p.session["frecuencias"])
        print("----------------Estoy en GET Presupuestar Frecuencias ")
        print(p.session["frecuencias"])
    return render(request, 'servicio/presupuestarFrecuencia.html', {'formset': formset, 'presupuesto': p})

@login_required
def presupuestarConfirmar(request):
    datos_cliente = PresupuestoSession.getOrCreate(request.session)
    tipos_servicios = PresupuestoSession.getTipoServicio(request.session)
    frecuencias = PresupuestoSession.getFrecuencia(request.session)
    servicio_pk = request.session.get("servicio_pk")
    importe_total = 0
    importe_sugerido = 0
    importe = {}
    if (request.method == 'POST'):
        form = FormConfirmar(request.POST)  
        if form.is_valid():
            if form.cleaned_data['cantidad_empleados'] <= 0:
                form.add_error('cantidad_empleados', 'No se puede calcular con 0 o menos valores')
                return render(request, 'servicio/presupuestarConfirmar.html', {'form': form, 'presupuesto': datos_cliente, 'tipo_Servicios': tipos_servicios, 'frecuencias': frecuencias, 'importe_sugerido': importe_sugerido, 'importe_total': importe_total})
            new_servicio = saveServicio(datos_cliente, form.cleaned_data, form.cleaned_data['importe_total'], servicio_pk)
            saveTipoServicios(new_servicio, tipos_servicios, servicio_pk)
            saveFrecuenca(new_servicio, frecuencias, servicio_pk)
            request.session['presupuesto'] = {}
            request.session['servicios'] = []
            request.session['frecuencias'] = []
            request.session['servicio_pk'] = None
            if servicio_pk == None:
                return redirect('presupuestarImprimir', new_servicio.pk)
            else:    
                return redirect('presupuestarModificarImprimir', servicio_pk)
    else:
        if servicio_pk != None and len(request.GET) == 0: 
            servicio = Servicio.objects.get(pk=servicio_pk)
            form = FormConfirmar(initial={'porcentaje': servicio.porcentaje, 'cantidad_empleados': servicio.cant_empleados})    
            importe = calcularImportePresupuesto(tipos_servicios, servicio.cant_empleados, len(frecuencias), datos_cliente['tipo'])
            importe_total = calcularPorcentaje(importe['importe_sugerido'], servicio.porcentaje)
        else:
            form = FormConfirmar()    
            print(len(request.GET))
            if len(request.GET) > 0:
                form = FormConfirmar(request.GET)
                if int(request.GET['cantidad_empleados']) >= 1 :
                    cant_empleados = int(request.GET['cantidad_empleados'])
                    print("Cantidad de empleados que vienen en la request: " + request.GET['cantidad_empleados'])
                    importe = calcularImportePresupuesto(tipos_servicios, cant_empleados, len(frecuencias), datos_cliente['tipo'])
                    if 'porcentaje' in request.GET and int(request.GET['porcentaje']) != 0:
                        importe_total = calcularPorcentaje(importe['importe_sugerido'], int(request.GET['porcentaje']))
                        print(importe_total)
                    else:
                        importe_total = importe['importe_sugerido']
                    response_data = {
                        'importe_total': importe_total,
                    }
                    print("Importe en forma de json que devuelve la funcion cuando se hace la peticion ajax: " + str(response_data['importe_total']))
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({'error': 'Debe ingresar al menos 1 empleado'})
                    # TODO: PREGUNTAR PORQUE DEVUELVE LOS VALORES ESOS COMO IMPORTE_TOTAL INICIALIZADOS EN 0? YA QUE NO TIENE SENTIDO CREO
                    #return render(request, 'servicio/presupuestarConfirmar.html', {'form': form, 'presupuesto': datos_cliente, 'tipo_Servicios': tipos_servicios, 'frecuencias': frecuencias, 'importe_sugerido': 0, 'importe_total': 0, 'total_servicios': 0, 'mano_obra': 0})
            else:
                importe = calcularImportePresupuesto(tipos_servicios, form.fields['cantidad_empleados'].initial, len(frecuencias), datos_cliente['tipo'])
                importe_total = importe['importe_sugerido']

        total_servicios = locale.currency(importe['total_servicios'], grouping=True)
        porcentaje_ganancia = locale.currency(importe['porcentaje_ganancia'], grouping=True)
        mano_obra = locale.currency(importe['mano_obra_servicio'], grouping=True)
        importe_sugerido = "{:.2f}".format(importe['importe_sugerido'])
        importe_total_formateado = locale.currency(importe_total, grouping=True)
        importe_total = "{:.2f}".format(importe_total)
            
    return render(request, 'servicio/presupuestarConfirmar.html', {
        'form': form, 
        'presupuesto': datos_cliente, 
        'tipo_Servicios': tipos_servicios, 
        'frecuencias': frecuencias, 
        'importe_sugerido': importe_sugerido, 
        'importe_total': importe_total, 
        'total_servicios': total_servicios, 
        'mano_obra': mano_obra, 
        'fecha_actual': timezone.now().date(),
        'importe_total_formateado':importe_total_formateado,
        'porcentaje_ganancia':porcentaje_ganancia}
    )

@login_required
def presupuestarImprimir(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    return render(request, 'servicio/presupuestarImprimir.html', {'servicio': servicio})

@login_required
def detalleServicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    tipos_servicios = CantServicioTipoServicio.objects.filter(servicio=servicio)
    frecuencias = Frecuencia.objects.filter(servicio=servicio)
    empleados_frecuencias = Empleado.objects.filter(frecuencias__in=frecuencias)
    return render(request, 'servicio/detalleServicio.html', {'servicio': servicio, 'tipoServicios': tipos_servicios, 'frecuencias': frecuencias,'empleados':empleados_frecuencias})

@login_required
def pdfImprimir(request, pk):
    subtotal = 0
    servicio = Servicio.objects.get(pk=pk)
    lista_frecuencias = Frecuencia.objects.filter(servicio=servicio)
    lista_tipos_servicios = CantServicioTipoServicio.objects.filter(servicio=servicio)
    for tipo in lista_tipos_servicios: 
        tipo_Servicio = TipoServicio.habilitados.get(pk=tipo.tipoServicio.pk)
        subtotal = subtotal + tipo_Servicio.getPrecio(tipo.cantidad)
    return render(request   , 'servicio/pdfImprimir.html', {'servicio': servicio, 'frecuencias': lista_frecuencias, 'tipoServicios': lista_tipos_servicios, 'subtotal' : subtotal})

@method_decorator(login_required, name='dispatch')
class contratarServicio(UpdateView):
    model = Servicio
    form_class = FormContratarServicio
    template_name = 'servicio/contratarServicio.html'
    success_url = reverse_lazy('asignarEmpleados', kwargs={'pk': model.pk})

    def get_success_url(self):
        return reverse_lazy('asignarEmpleados', kwargs={'pk': self.object.pk})

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        if self.object.estado != 1:
            return redirect('errorServicio')
        return super().get(request, *args, **kwargs)

@login_required
def contratarServicioCorrecto(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    return render(request, 'servicio/contratarOpciones.html', {'servicio': servicio})

@method_decorator(login_required, name='dispatch')
class errorServicio(TemplateView):
    template_name = 'servicio/errorServicio.html'

@login_required
def asignarEmpleados(request, pk):
    if request.method == 'POST':
        formset = formset_factory(FormAsignarEmpleados)
        formset = formset(request.POST)
        servicio = Servicio.objects.get(pk=pk)
        print(formset)
        if formset.is_valid():
            for form in formset:
                frecuencia = form.cleaned_data['frecuencia']
                empleados = form.cleaned_data['empleados']
                if empleados.count() != servicio.cant_empleados:
                    form.add_error('empleados', 'Solo se pueden asignar ' + str(servicio.cant_empleados) + ' empleados')
                    form.fields['empleados'].choices = [(empleado.pk, empleado.nombre +' '+empleado.apellido) for empleado in form.fields['empleados'].queryset]
                    return render(request, 'servicio/asignarEmpleados.html', {'formset': formset, 'servicio': servicio})
                frecuencia = Frecuencia.objects.get(pk=frecuencia.pk)
                for empleado in empleados:
                    frecuencia.empleados.add(empleado.pk)
                    servicio.empleado.add(empleado.pk)
                frecuencia.save()
                servicio.save()
            if servicio.cliente.tipo == 2:
                servicio.estado = 3
                servicio.save()
                return redirect('contratarServicioCorrecto', pk)
            return redirect('crearFacturaSeña', pk)
    else:
        servicio = Servicio.objects.get(pk=pk)
        frecuencias = Frecuencia.objects.filter(servicio=servicio)
        formset_inicial = formset_factory(FormAsignarEmpleados,extra=len(frecuencias))
        print(frecuencias)
        formset = formset_inicial()
        for form, frecuencia in zip(formset, frecuencias):
            form.fields['frecuencia'].choices = [(frecuencia.pk, frecuencia.get_dia_display() + ' - ' + frecuencia.get_turno_display())]
            form.fields['frecuencia'].initial = frecuencia.pk
            form.fields['empleados'].queryset = Empleado.habilitados.disponibles(servicio.fecha_inicio,servicio.fecha_finaliza, frecuencia.dia, frecuencia.turno)
            form.fields['empleados'].choices = [(empleado.pk, empleado.nombre +' '+empleado.apellido) for empleado in form.fields['empleados'].queryset]
        context = {
            'formset': formset,
            'servicio': servicio,
        }
        return render(request, 'servicio/asignarEmpleados.html', context)