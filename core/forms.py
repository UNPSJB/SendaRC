from django import forms
import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field, HTML
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
        super(ClienteForm, self).__init__(*args, **kwargs)
        if is_modificar:
            mensaje = 'Modificar un cliente aquí. Dale clic en guardar al terminar'
            self.fields['tipo'].widget.attrs['hidden'] = False
        else:
            mensaje = 'Agregar un cliente aquí. Dale clic en guardar al terminar'
            self.fields['tipo'].widget.attrs['hidden'] = True
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
    
    def clean(self):
        cleaned_data = super().clean()
        cuil= str(cleaned_data.get('cuil', ''))
        telefono = str(cleaned_data.get('telefono', ''))

        regex_pattern_cuil = r'^\d{11}$'
        regex_pattern_telefono = r'^\d{10}$'

        if not re.match(regex_pattern_cuil, cuil):
            self.add_error('cuil', "Formato requerido(sin guiones): xx-xxxxxxxx-x")

        if not re.match(regex_pattern_telefono, telefono):
            self.add_error('telefono', "Formato requerido(sin guiones): codigoArea-número")

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['descripcion', 'unidad_medida', 'precio', 'insumos', 'maquinarias']
        widgets = {
            'insumos': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'maquinarias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Agregue los nuevos datos del tipo de servicio. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agrega los datos de un nuevo tipo de servicio. Dale clic en guardar al terminar'
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['insumos'].queryset = Insumo.objects.all()
        self.fields['maquinarias'].queryset = Maquinaria.objects.all()

        self.fields['insumos'].widget.choices = [(insumo.pk, insumo.descripcion) for insumo in Insumo.objects.all()]
        self.fields['maquinarias'].widget.choices = [(maquinaria.pk, maquinaria.nombre) for maquinaria in Maquinaria.objects.all()]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(
                        'Datos Tipos de servicio.'
                    ),
                    Div(
                        FloatingField('descripcion'),
                        FloatingField('unidad_medida'),
                        FloatingField('precio'),
                        css_class='container-inputs'
                    ),
                    Div(
                        Field('insumos', multiple=True, css_class='form-control'),
                        Field('maquinarias', multiple=True, css_class='form-control'),    
                        css_class='container-inputs'
                    )
                ),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-Guardar'),
                HTML('<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Cancelar</a>'),
                css_class='input-group mb-3 operaciones'
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
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar maquinaria aquí. Dale clic en guardar al terminar'
        else:
            mensaje = 'Agregar maquinaria aquí. Dale clic en guardar al terminar'
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
                    HTML('<a href="{% url "gestionMaquinaria" %}" class="btn-Cancelar">Cancelar</a>'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )
