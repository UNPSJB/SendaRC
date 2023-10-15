from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import *

class FormSancion(forms.ModelForm):
    class Meta:
        model = Sancion
        fields = ['tipo', 'nroSancion', 'empleado']
            
    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar una sancion aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar una sancion aquí. Dale clic en guardar al terminar'
        super(FormSancion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(
                        
                    ),
                    Div(
                        FloatingField('tipo'),
                        FloatingField('nroSancion'),
                        FloatingField('empleado'),
                        css_class='container-inputs-form'
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionSanciones" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )

class FormEmpleado(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['numDNI', 'numLegajo', 'nombre', 'apellido', 'telefono', 'email', 'sueldo', 'localidad']
        
    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar un empleado aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar un empleado aquí. Dale clic en guardar al terminar'
        super(FormEmpleado, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(

                    ),
                    Div(
                        FloatingField('numDNI'),
                        FloatingField('numLegajo'),
                        FloatingField('nombre'),
                        FloatingField('apellido'),
                        FloatingField('telefono'),
                        FloatingField('email'),
                        FloatingField('sueldo'),
                        FloatingField('localidad'),
                        css_class='container-inputs-form'
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionEmpleado" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )

class FormLocalidad(forms.ModelForm):
    class Meta:
        model = Localidad
        fields = ['cp', 'nombre']
    
    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar una localidad aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar una localidad aquí. Dale clic en guardar al terminar'
        super(FormLocalidad, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(
                        
                    ),
                    Div(
                        FloatingField('cp'),
                        FloatingField('nombre'),
                        css_class='container-inputs-form'
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionLocalidad" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )    

class FormInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med', 'contenido_neto', 'marca', 'cantidad']
       
    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar un insumo aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar un insumo aquí. Dale clic en guardar al terminar'
        super(FormInsumo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(
                        
                    ),
                    Div(
                        FloatingField('descripcion'),
                        FloatingField('unidad_med'),
                        FloatingField('contenido_neto'),
                        FloatingField('marca'),
                        FloatingField('cantidad'),
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionInsumos" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )
    

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cuil', 'nombre', 'apellido', 'direccion', 'tipo', 'tipoPersona', 'telefono', 'email', 'localidad']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar un cliente aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar un cliente aquí. Dale clic en guardar al terminar'
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(

                    ),
                    Div(
                        FloatingField('cuil'),
                        FloatingField('nombre'),
                        FloatingField('apellido'),
                        FloatingField('direccion'),
                        FloatingField('tipo'),
                        FloatingField('tipoPersona'),
                        FloatingField('telefono'),
                        FloatingField('email'),
                        FloatingField('localidad'),
                        css_class='container-inputs-form'
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionClientes" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['descripcion', 'unidad_medida', 'precio', 'insumos', 'maquinarias']
    
    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    Div(
                        'Alta Servicio',
                        css_class='input-group mb-3 info-formulario'
                    ),
                Div(
                    FloatingField('descripcion'),
                    FloatingField('unidad_medida'),
                    FloatingField('precio'),
                    FloatingField('insumos'),
                    FloatingField('maquinarias'),
                    css_class='container-inputs'
                ),
            ),
            Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Cancelar</a>'),
                css_class='input-group mb-3 operaciones'
            )
        )
    )
class FormAltaMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['nombre', 'modelo', 'marca', 'cantidad', 'observaciones', 'baja']
        widgets = {
            "nombre": forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre'}),
            "modelo": forms.TextInput(attrs={'class': 'form-control','placeholder':'Modelo'}),
            "marca": forms.TextInput(attrs={'class': 'form-control','placeholder':'Marca'}),
            "cantidad": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Cantidad'}),
            "observaciones": forms.Textarea(attrs={'class': 'form-control textarea','placeholder':'Observaciones'}),
            "estado": forms.BooleanField()
        }
    
    def __init__(self, *args, **kwargs):
        super(FormAltaMaquinaria, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">Agrega una maquinaria aquí. Dale click en agregar al finalizar</p>'),
                Fieldset(
                    Div(
                        'Agrega una maquinaria aquí. Dale click en agregar al finalizar'
                    ),
                    Div(
                        FloatingField('nombre'),
                        FloatingField('modelo'),
                        FloatingField('marca'),
                        FloatingField('cantidad'),
                        FloatingField('observaciones'),
                        FloatingField('estado')
                    )
                ),
                Div(
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    HTML('<a href="#" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )    