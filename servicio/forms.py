from typing import Any
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, HTML, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import ValidationError, formset_factory, modelformset_factory, ModelMultipleChoiceField, CheckboxSelectMultiple
from datetime import datetime
from core.models import *
from .models import *


class FormPresupuestoCliente(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'direccion', 'metros2', 'observaciones', 'tipo']

    def __init__(self, *args, **kwargs):
        super(FormPresupuestoCliente, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.habilitados.all()
        self.fields['cliente'].widget.choices = [
            (cliente.pk, cliente.cuil+' | '+cliente.nombre+' '+cliente.apellido) for cliente in Cliente.habilitados.all()]
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
                            '<a href="{% url "gestionServicios" %}" class="btn-Cancelar">Cancelar</a>'),
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
        self.fields['tipo_servicio'].choices = [(tipo.id, f'{tipo.descripcion} - {tipo.getUnidadMedida()}') for tipo in TipoServicio.objects.all()]
        

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
    porcentaje = forms.IntegerField(label='Porcentaje declarado (opcional)', required=False)
    cantidad_empleados = forms.IntegerField(label='Cantidad de Empleados por Turno')
    importe_sugerido = forms.FloatField(widget=forms.HiddenInput())
    importe_total = forms.FloatField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['porcentaje'].initial = 0
        self.fields['cantidad_empleados'].initial = 1
    
class FormContratarServicio(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_finaliza = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Servicio
        fields = ['fecha_inicio', 'fecha_finaliza']

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_finaliza = cleaned_data.get('fecha_finaliza')

        if fecha_inicio and fecha_finaliza:
            if fecha_inicio > fecha_finaliza:
                raise ValidationError(('La fecha de finalización no puede ser anterior a la de inicio'))
            if fecha_inicio < self.instance.fecha_emision:
                raise ValidationError(('La fecha de inicio no puede ser anterior a la fecha de emisión'))
            if self.instance.tipo == 1 and fecha_inicio != fecha_finaliza:
                raise ValidationError('Este servicio es eventual, la fecha de inicio debe ser igual al final')
        return cleaned_data
    
    def save(self, commit: bool = ...) -> Any:
        self.instance.estado = 3
        return super().save(commit)
   
class FormAsignarEmpleados(forms.Form):
    frecuencia = forms.ModelChoiceField(label='Frecuencia', queryset=Frecuencia.objects.all(), widget=forms.Select(attrs={'class': 'input'}))
    empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'input'}),
        label='Empleados'
    )
    