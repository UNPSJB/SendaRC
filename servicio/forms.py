from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field, HTML, ButtonHolder
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import formset_factory, modelformset_factory, ModelMultipleChoiceField, CheckboxSelectMultiple
from core.models import *
from .models import *


class FormPresupuestoCliente(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'direccion', 'metros2', 'observaciones', 'tipo']

    def __init__(self, *args, **kwargs):
        super(FormPresupuestoCliente, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].widget.choices = [
            (cliente.pk, cliente.cuil+' | '+cliente.nombre+' '+cliente.apellido) for cliente in Cliente.objects.all()]
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    Div(

                    ),
                    Div(
                        Field('cliente'),
                        FloatingField('tipo'),
                        FloatingField('direccion'),
                        FloatingField('metros2'),
                        FloatingField('observaciones'),
                        css_class='container-inputs'
                    ),
                    Div(
                        HTML(
                            '<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Cancelar</a>'),
                        Submit('submit', 'Siguiente', css_class='btn-Guardar'),
                        css_class='input-group mb-3 operaciones'
                    )

                )
            )
        )

class FormBaseTipoServicio(forms.Form):
    tipo_servicio = forms.ModelChoiceField(
        queryset=TipoServicio.objects.all(),
        widget=forms.Select(attrs={'class': 'input'}),
        label='Tipo de Servicio'
    )
    cantidad = forms.IntegerField(label='Cantidad')
    
    def __init__(self, *args, **kwargs):
        super(FormBaseTipoServicio, self).__init__(*args, **kwargs)
        self.fields['tipo_servicio'].choices = [(tipo.id, tipo.descripcion) for tipo in TipoServicio.objects.all()]
        

class FormBaseFrecuencia(forms.Form):
    dia = forms.ChoiceField(
        choices=Frecuencia.DIA,
        widget=forms.Select(attrs={'class': 'input'}),
        label='Dia'
    )
    turno = forms.ChoiceField(
        choices=Frecuencia.TURNO,
        widget=forms.Select(attrs={'class': 'input'}),
        label='Turno'
    )
    
class FormConfirmar(forms.Form):
    porcentaje = forms.CharField(label='Porcentaje declarado')

