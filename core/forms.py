from typing import Any
from django import forms
import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from localflavor.ar.forms import ARCUITField, ARDNIField, ARPostalCodeField

from .models import *


class FormSancion(forms.ModelForm):
    class Meta:
        model = Sancion
        fields = ['tipo', 'nroSancion', 'empleado']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar una sancion aquí. Dale click en guardar al terminar'
        else:
            mensaje = 'Agregar una sancion aquí. Dale click en guardar al terminar'
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
                    HTML(
                        '<a href="{% url "gestionSanciones" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )


class FormEmpleado(forms.ModelForm):
    numDNI = ARDNIField(label='DNI', error_messages={
                        'invalid': 'DNI no válido'})

    class Meta:
        model = Empleado
        fields = ['numDNI', 'nombre', 'apellido', 'telefono',
                  'email', 'sueldo', 'localidad', 'activo']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar un empleado aquí. Dale click en guardar al terminar'
        else:
            mensaje = 'Agregar un empleado aquí. Dale click en guardar al terminar'
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
                        FloatingField('nombre'),
                        FloatingField('apellido'),
                        FloatingField('telefono'),
                        FloatingField('email'),
                        FloatingField('sueldo'),
                        FloatingField('localidad'),
                        Field('activo'),
                        css_class='container-inputs-form'
                    )
                ),
                Div(
                    HTML(
                        '<a href="{% url "gestionEmpleado" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )


class FormLocalidad(forms.ModelForm):
    cp = ARPostalCodeField(label='Codigo Postal', error_messages={
                           'invalid': 'Codigo postal no válido'})

    class Meta:
        model = Localidad
        fields = ['cp', 'nombre']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar una localidad aquí. Dale click en guardar al terminar'
        else:
            mensaje = 'Agregar una localidad aquí. Dale click en guardar al terminar'
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
                    HTML(
                        '<a href="{% url "gestionLocalidad" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )


class FormInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med',
                  'contenido_neto', 'marca', 'cantidad', 'activo']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar un insumo aquí. Dale click en guardar al terminar'
        else:
            mensaje = 'Agregar un insumo aquí. Dale click en guardar al terminar'
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
                        Field('activo')
                    )
                ),
                Div(
                    HTML(
                        '<a href="{% url "gestionInsumos" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )


class ClienteForm(forms.ModelForm):
    cuil = ARCUITField(label='CUIL', error_messages={
                       'invalid': 'CUIL no válido'})

    class Meta:
        model = Cliente
        fields = ['cuil', 'nombre', 'apellido', 'direccion', 'tipo',
                  'tipoPersona', 'telefono', 'email', 'localidad', 'activo']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        super(ClienteForm, self).__init__(*args, **kwargs)

        if is_modificar:
            mensaje = 'Modificar un cliente aquí. Dale click en guardar al terminar'
            self.fields['tipo'].widget.attrs['hidden'] = False
            div_class = 'container-inputs-form'
        else:
            mensaje = 'Agregar un cliente aquí. Dale click en guardar al terminar'
            self.fields['tipo'].widget.attrs['hidden'] = True
            div_class = 'container-inputs-form ocultar'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(),
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
                        Field('activo'),
                        css_class=div_class
                    )
                ),
                Div(
                    HTML('<a href="{% url "gestionClientes" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                    ),
                css_class='container-forms'
            )
        )


class TipoServicioForm(forms.ModelForm):

    class Meta:
        model = TipoServicio
        fields = ['descripcion', 'unidad_medida',
                  'precio', 'insumos', 'maquinarias', 'activo']

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        if is_modificar:
            mensaje = 'Agregue los nuevos datos del tipo de servicio. Dale click en guardar al terminar'
        else:
            mensaje = 'Agrega los datos de un nuevo tipo de servicio. Dale click en guardar al terminar'

        self.fields['insumos'].queryset = Insumo.habilitados.all()
        self.fields['maquinarias'].queryset = Maquinaria.objects.all()

        self.fields['insumos'].widget.choices = [
            (insumo.pk, insumo.descripcion) for insumo in Insumo.habilitados.all()]
        self.fields['maquinarias'].widget.choices = [
            (maquinaria.pk, maquinaria.nombre) for maquinaria in Maquinaria.objects.all()]
        self.fields['maquinarias'].required = False
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
                        Field('insumos', multiple=True),
                        Field('maquinarias', multiple=True),
                        Field('activo'),
                        css_class='container-inputs'
                    )
                ),
            ),
            Div(
                HTML(
                    '<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Cancelar</a>'),
                Submit('submit', 'Guardar', css_class='btn-Guardar'),
                css_class='input-group mb-3 operaciones'
            )
        )


class FormAltaMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['nombre', 'modelo', 'marca',
                  'cantidad', 'activo', 'observaciones']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop('is_modificar', False)
        if is_modificar:
            mensaje = 'Modificar maquinaria aquí. Dale click en guardar al terminar'
        else:
            mensaje = 'Agregar maquinaria aquí. Dale click en guardar al terminar'
        super(FormAltaMaquinaria, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML(
                    '<p class="info-formulario">Agrega una maquinaria aquí. Dale click en agregar al finalizar</p>'),
                Fieldset(
                    Div(
                        'Agrega una maquinaria aquí. Dale click en agregar al finalizar'
                    ),
                    Div(
                        FloatingField('nombre'),
                        FloatingField('modelo'),
                        FloatingField('marca'),
                        FloatingField('cantidad'),
                        Field('activo'),
                        FloatingField('observaciones'),
                    )
                ),
                Div(
                    HTML(
                        '<a href="{% url "gestionMaquinaria" %}" class="btn-Cancelar">Cancelar</a>'),
                    Submit('submit', 'Guardar', css_class='btn-Guardar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )


class FiltroClientesForm(forms.Form):
    ESTADOS = [('Activos', 'Activos'), ('No activos',
                                        'No activos'), ('Todos', 'Todos')]
    TIPOS_PERSONA = [('', '---'), ('1', 'Particular'), ('2', 'Juridico')]
    TIPOS = [('', '---'), ('1', 'Ocasional'), ('2', 'Habitual')]

    estado = forms.ChoiceField(choices=ESTADOS, required=False)
    tipo_persona = forms.ChoiceField(choices=TIPOS_PERSONA, required=False)
    tipo = forms.ChoiceField(choices=TIPOS, required=False)

    def __init__(self, *args, **kwargs):
        super(FiltroClientesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field(
                    'estado', css_class='form-select form-select-sm form-select-filter'),
                Field('tipo_persona',
                      css_class='form-select form-select-sm form-select-filter'),
                Field(
                    'tipo', css_class='form-select form-select-sm form-select-filter mb-0'),
                css_class='contenedorFiltersForm'
            )
        )

class FiltroActivoForm(forms.Form):
    ESTADOS = [('Activos', 'Activos'), ('No activos',
                                        'No activos'), ('Todos', 'Todos')]
    estado = forms.ChoiceField(choices=ESTADOS, required=False)

    def __init__(self, *args, **kwargs):
        super(FiltroActivoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field(
                    'estado', css_class='form-select form-select-sm form-select-filter'),
                css_class='contenedorFiltersForm'
            )
        )