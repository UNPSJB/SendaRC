from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import *

class FormAltaInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med', 'contenido_neto', 'marca', 'cantidad']
    
    def __init__(self, *args, **kwargs):
        super(FormAltaInsumo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
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
        fields = ['cuil','nombre', 'apellido', 'direccion', 'tipo', 'tipoPersona','telefono','email','localidad']

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    Div(
                        'Agrega un cliente aquí. Dale click en agregar al finalizar'
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