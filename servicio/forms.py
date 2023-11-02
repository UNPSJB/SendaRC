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
                            '<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Volver</a>'),
                        Submit('submit', 'Siguiente', css_class='btn-Guardar'),
                        css_class='input-group mb-3 operaciones'
                    )

                )
            )
        )

class FormServicios(forms.ModelForm):
    tipoServicios = forms.ModelMultipleChoiceField(queryset=TipoServicio.objects.all(), widget=CheckboxSelectMultiple)
    class Meta:
        model = Servicio
        fields = ["tipoServicios"]

    def __init__(self, *args, **kwargs):
        super(FormServicios, self).__init__(*args, **kwargs)
        self.fields['tipoServicios'].widget.choices = [
            (TipoServicio.pk, TipoServicio.descripcion) for TipoServicio in TipoServicio.objects.all()]
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('tipoServicios'),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='btn-Guardar')
            )
        )

class FormFrecuencias(forms.ModelForm):
    class Meta:
        model = Frecuencia
        fields = ['dia', 'turno']

    def __init__(self, *args, **kwargs):
        super(FormPresupuestoFrecuencias, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    Div(

                    ),
                    Div(
                        FloatingField('dia'),
                        FloatingField('turno'),
                        HTML('Horario: <span id="textoHora">-</span>'),
                        css_class='container-inputs'
                    ),
                    Div(
                        HTML(
                            '<a href="{% url "gestionTipoServicio" %}" class="btn-Cancelar">Volver</a>'),
                        Submit('submit', 'Agregar', css_class='btn-Guardar'),
                        Submit('submit', 'Siguiente', css_class='btn-Guardar'),
                        css_class='input-group mb-3 operaciones'
                    )

                )
            )
        )
