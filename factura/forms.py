from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import *

class SelectClienteForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.habilitados.all(),
        widget=forms.Select(attrs={'class': 'input'}),
        label='Seleciona Cliente'
    )
    
    def __init__(self, *args, **kwargs):
        super(SelectClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].choices = [(cliente.id, f'{cliente.nombre} {cliente.apellido} - {cliente.cuil}') for cliente in Cliente.habilitados.all()]
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field('cliente', css_class='form-select form-select-sm form-select-filter'),
                Submit('submit', 'Ver servicios', css_class='btn-filtrar'),
                css_class='contenedorFiltersForm'
            )
        )
        
class FormaPagoForm(forms.Form):
    ESTADOS = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')]
    #ESTADOS = [('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('Cheques', 'Cheques')]

    forma = forms.ChoiceField(choices=ESTADOS, required=False)

    def __init__(self, *args, **kwargs):
        super(FormaPagoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field('forma', css_class='form-select form-select-sm form-select-filter'),
                css_class='contenedor-select-btn'
            )
        )

class FormCobroFacturaSeña(forms.Form):
    formapago = forms.ChoiceField(choices=[(3, 'Transferencia'), (2, 'Cheque'), (1, 'Efectivo')])
