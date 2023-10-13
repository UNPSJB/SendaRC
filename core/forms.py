from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import *

class FormAltaInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med', 'contenido_neto', 'marca', 'cantidad']
        widgets = {
            "descripcion": forms.TextInput(attrs={'class': 'form-control textinput','placeholder':'Descripción'}),
            "unidad_med": forms.Select(attrs={'class': 'form-select'}),
            "contenido_neto": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Contenido neto'}),
            "marca": forms.TextInput(attrs={'class': 'form-control','placeholder':'Marca'}),
            "cantidad": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Cantidad'})
        }

    def __init__(self, *args, **kwargs):
        super(FormAltaInsumo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">Agrega un insumo aquí. Dale click en agregar al finalizar</p>'),
                Fieldset(
                    Div(
                        'Agrega un insumo aquí. Dale click en agregar al finalizar'
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
                    Submit('submit', 'Guardar', css_class='btn-Agregar'),
                    Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )
        
class FormModificarInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med', 'contenido_neto', 'marca', 'cantidad']
        widgets = {
            "descripcion": forms.Textarea(attrs={'class': 'form-control textarea','placeholder':'Decripción'}),
            "unidad_med": forms.Select(attrs={'class': 'form-select','placeholder':'Unidad de medida'}),
            "contenido_neto": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Contenido neto'}),
            "marca": forms.TextInput(attrs={'class': 'form-control','placeholder':'Marca'}),
            "cantidad": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Cantidad'})
        }
    """ Para agregar campo adicion que no es de Insumo
    def save(self, commit=True):
        insumo = super().save(commit=commit)
        if self.cleaned_data['incrementar']:
            insumo.cantidad += 10
            insumo.save()
        return insumo
    """
    def __init__(self, *args, **kwargs):
        super(FormModificarInsumo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">Modificar un insumo aquí. Dale click en guardar al finalizar</p>'),
                Fieldset(
                    Div(
                        'Agrega un insumo aquí. Dale click en agregar al finalizar'
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
                    Submit('submit', 'Agregar', css_class='btn-Agregar'),
                    Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
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
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['localidad'].to_field_name = 'nombre'
        self.fields['telefono'].widget.attrs['input_type'] = 'tel'
        self.helper.layout = Layout(
            Div(
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
                    Submit('submit', 'Agregar', css_class='btn-Agregar'),
                    Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
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
                Submit('submit', 'Guardar', css_class='btn-Agregar'),
                Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
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
            "observaciones": forms.TextInput(attrs={'class': 'form-control textarea','placeholder':'Observaciones'}),
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
                    Submit('submit', 'Agregar', css_class='btn-Agregar'),
                    Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
                    css_class='input-group mb-3 operaciones'
                ),
                css_class='container-forms'
            )
        )    