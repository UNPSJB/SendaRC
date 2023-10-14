from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
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
                        'Alta Insumo'
                    ),
                    Div(
                        FloatingField('descripcion'),
                        FloatingField('unidad_med'),
                        FloatingField('contenido_neto'),
                        FloatingField('marca'),
                        FloatingField('cantidad'),
                        css_class='container-inputs'
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
            Fieldset(
                Div(
                    'Alta Cliente',
                    css_class='input-group mb-3 info-formulario'
                ),
                Div(
                    FloatingField('cuil'),
                    FloatingField('nombre'),
                    FloatingField('apellido'),
                    FloatingField('direccion'),
                    FloatingField('tipo'),
                    FloatingField('tipoPersona', class_name='select-form'),
                    FloatingField('telefono'),
                    FloatingField('email'),
                    FloatingField('localidad'),
                    css_class='container-inputs'
                ),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-Agregar'),
                Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
                css_class='input-group mb-3 operaciones'
            )
        )

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['descripcion', 'unidad_medida', 'precio', 'insumos', 'maquinarias']
        widgets = {
            'insumos': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'maquinarias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['insumos'].queryset = Insumo.objects.all()
        self.fields['maquinarias'].queryset = Maquinaria.objects.all()

        self.fields['insumos'].widget.choices = [(insumo.codigo, insumo.descripcion) for insumo in Insumo.objects.all()]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                Div(
                    'Alta Servicio',
                    css_class='input-group mb-3 info-formulario'
                ),
                Div(
                    FloatingField('descripcion'),
                    FloatingField('unidad_medida'),
                    FloatingField('precio'),
                    css_class='container-inputs'
                ),
                Row(
                    Field('insumos', multiple=True, css_class='form-control'),
                    Field('maquinarias', multiple=True, css_class='form-control'),    
                    css_class='container-inputs'
                )
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-Agregar'),
                Submit('cancel', 'Cancelar', css_class='btn-Agregar'),
                css_class='input-group mb-3 operaciones'
            )
        )