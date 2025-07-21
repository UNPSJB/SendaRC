from typing import Any
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Hidden,
    Layout,
    Fieldset,
    Div,
    Field,
    Button,
    HTML,
    Submit,
)
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import (
    ValidationError,
    formset_factory,
    modelformset_factory,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)
from datetime import datetime
from core.models import *
from .models import *


class FiltrosServiciosForm(forms.Form):
    ESTADOS = [("", "Todos"), *Servicio.ESTADO]
    TIPO = [("", "---"), *Servicio.TIPO]

    estado = forms.ChoiceField(choices=ESTADOS, required=False)
    tipo = forms.ChoiceField(choices=TIPO, required=False)

    fecha_inicio = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    fecha_finaliza = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    limpiar_fecha_inicio = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Div(
                Field(
                    "estado", css_class="form-select form-select-sm form-select-filter"
                ),
                Field(
                    "tipo",
                    css_class="form-select form-select-sm form-select-filter mb-0",
                ),
                Field(
                    "fecha_inicio",
                    css_class="form-control form-control-sm form-select-filter",
                ),
                Field(
                    "fecha_finaliza",
                    css_class="form-control form-control-sm form-select-filter",
                ),
                css_class="d-flex gap-2",
            )
        )


class FormPresupuestoCliente(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "cliente",
            "direccion",
            "metros2",
            "observaciones",
            "tipo",
            "localidad",
        ]
        widgets = {
            "cliente": forms.Select(
                attrs={"class": "form-select", "placeholder": "Seleccionar Cliente"}
            ),
            "tipo": forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "Seleccionar Tipo de Servicio",
                }
            ),
            "localidad": forms.Select(
                attrs={"class": "form-select", "placeholder": "Seleccionar Localidad"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dirección"}
            ),
            "metros2": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Metros²",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cliente"].queryset = Cliente.habilitados.all()
        self.fields["localidad"].queryset = Localidad.objects.all()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False  # <-- sin labels duplicados

        self.helper.layout = Layout(
            Div(
                # Cliente
                Div(
                    HTML(label_cliente),
                    Field("cliente"),
                    css_class="col-md-12",
                ),
                # Tipo de Servicio
                Div(
                    HTML(label_tipo),
                    Field("tipo"),
                    css_class="col-md-6",
                ),
                # Localidad
                Div(
                    HTML(label_localidad),
                    Field("localidad"),
                    css_class="col-md-6",
                ),
                # Dirección
                Div(
                    HTML(label_direccion),
                    Field("direccion"),
                    css_class="col-md-12",
                ),
                # Metros²
                Div(
                    HTML(label_metros2),
                    Field("metros2"),
                    css_class="col-md-6",
                ),
                # Observaciones
                Div(
                    HTML(label_observaciones),
                    Field("observaciones"),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionServicios\' %}" class="btn btn-secondary">'
                    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
                    '<polyline points="15 18 9 12 15 6"></polyline></svg>'
                    " Cancelar</a>"
                ),
                Submit("submit", "Siguiente", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


# ---------- SVG labels (re-usable strings) ----------
label_cliente = """
<label for="{{ form.cliente.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
  </svg>
  Cliente
</label>
"""

label_tipo = """
<label for="{{ form.tipo.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <rect x="1" y="3" width="15" height="13"></rect>
    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
    <circle cx="5.5" cy="18.5" r="2.5"></circle>
    <circle cx="18.5" cy="18.5" r="2.5"></circle>
  </svg>
  Tipo de Servicio
</label>
"""

label_localidad = """
<label for="{{ form.localidad.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
    <circle cx="12" cy="10" r="3"></circle>
  </svg>
  Localidad
</label>
"""

label_direccion = """
<label for="{{ form.direccion.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
    <circle cx="12" cy="10" r="3"></circle>
  </svg>
  Dirección
</label>
"""

label_metros2 = """
<label for="{{ form.metros2.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
  </svg>
  Metros²
</label>
"""

label_observaciones = """
<label for="{{ form.observaciones.id_for_label }}" class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:0.5rem;">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
    <polyline points="14 2 14 8 20 8"></polyline>
  </svg>
  Observaciones
</label>
"""


class FormBaseTipoServicio(forms.Form):
    tipo_servicio = forms.ModelChoiceField(
        queryset=TipoServicio.habilitados.all(),
        empty_label=None,
        label="Tipo de Servicio",
        widget=forms.Select(attrs={"class": "form-select select2-tipo"}),
    )
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Cantidad",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Cantidad"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # prettier choices: "Descripción - Unidad"
        self.fields["tipo_servicio"].choices = [
            (tipo.id, f"{tipo.descripcion} – {tipo.getUnidadMedida()}")
            for tipo in TipoServicio.habilitados.all()
        ]

        # Asegurar que las clases CSS se apliquen
        self.fields["tipo_servicio"].widget.attrs.update(
            {"class": "form-select select2-tipo"}
        )
        self.fields["cantidad"].widget.attrs.update({"class": "form-control"})

        # --- crispy forms styling ---
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                # Tipo de Servicio
                Div(
                    HTML(label_tipo_servicio),
                    Field("tipo_servicio"),  # Sin css_class aquí
                    css_class="col-md-8",
                ),
                # Cantidad
                Div(
                    HTML(label_cantidad),
                    Field("cantidad"),  # Sin css_class aquí
                    css_class="col-md-4",
                ),
                css_class="row g-3 align-items-end",
            ),
        )


# ---------- SVG labels ----------
label_tipo_servicio = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <rect x="1" y="3" width="15" height="13"></rect>
    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
    <circle cx="5.5" cy="18.5" r="2.5"></circle>
    <circle cx="18.5" cy="18.5" r="2.5"></circle>
  </svg>
  Tipo de Servicio
</label>
"""

label_cantidad = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <line x1="12" y1="1" x2="12" y2="23"></line>
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
  </svg>
  Cantidad
</label>
"""


class FormBaseFrecuencia(forms.Form):
    dia = forms.ChoiceField(choices=[], label="Día")
    turno = forms.ChoiceField(choices=[], label="Turno")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["dia"].choices = [("", "Seleccione un día...")] + sorted(
            Frecuencia.DIA, key=lambda x: x[0]
        )
        self.fields["turno"].choices = [("", "Seleccione un turno...")] + sorted(
            Frecuencia.TURNO, key=lambda x: x[0]
        )

        self.fields["dia"].widget.attrs.update(
            {"class": "form-select", "required": True}
        )
        self.fields["turno"].widget.attrs.update(
            {"class": "form-select", "required": True}
        )

        self.helper = FormHelper()
        self.helper.form_tag = False  # porque el form lo incluye el template principal
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                HTML(label_dia),
                Field("dia"),
                css_class="col-md-6",
            ),
            Div(
                HTML(label_turno),
                Field("turno"),
                HTML('<div class="time-display mt-2"></div>'),
                css_class="col-md-6",
            ),
        )


# SVG labels ----------------------------------------------------
label_dia = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
    <line x1="16" y1="2" x2="16" y2="6"></line>
    <line x1="8" y1="2" x2="8" y2="6"></line>
    <line x1="3" y1="10" x2="21" y2="10"></line>
  </svg>
  Día
</label>
"""

label_turno = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <circle cx="12" cy="12" r="10"></circle>
    <polyline points="12,6 12,12 16,14"></polyline>
  </svg>
  Turno
</label>
"""


class FormConfirmar(forms.Form):
    porcentaje = forms.IntegerField(
        label="Porcentaje declarado (opcional)",
        required=False,
        max_value=100,
        initial=0,
    )
    cantidad_empleados = forms.IntegerField(
        label="Cantidad de Empleados por Turno",
        min_value=1,
        initial=1,
    )
    importe_sugerido = forms.FloatField(widget=forms.HiddenInput())
    importe_total = forms.FloatField(widget=forms.HiddenInput())
    nuevo_importe_total = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                # Porcentaje
                Div(
                    HTML(label_porcentaje),
                    Field("porcentaje", css_class="form-control", placeholder="0"),
                    HTML('<div class="form-text">De 0 a 100 %</div>'),
                    css_class="col-md-6",
                ),
                # Cantidad de empleados
                Div(
                    HTML(label_empleados),
                    Field(
                        "cantidad_empleados", css_class="form-control", placeholder="1"
                    ),
                    css_class="col-md-6",
                ),
                css_class="row g-3",
            ),
            Hidden("importe_sugerido", value="{{ importe_sugerido }}"),
            Hidden("importe_total", value="{{ importe_total }}"),
            Hidden("nuevo_importe_total", value="{{ nuevo_importe_total|default:'' }}"),
        )


# SVG labels ----------------------------------------------------
label_porcentaje = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <line x1="19" y1="5" x2="5" y2="19"></line>
    <circle cx="6.5" cy="6.5" r="2.5"></circle>
    <circle cx="17.5" cy="17.5" r="2.5"></circle>
  </svg>
  Porcentaje declarado
</label>
"""

label_empleados = """
<label class="form-label">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
       style="margin-right:.4rem; vertical-align:text-bottom;">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
    <circle cx="9" cy="7" r="4"></circle>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
  </svg>
  Empleados por Turno
</label>
"""


class FormContratarServicio(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_finaliza = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Servicio
        fields = ["fecha_inicio", "fecha_finaliza"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.tipo == 1:
            self.fields["fecha_finaliza"].required = False
            self.fields["fecha_finaliza"].widget.attrs["hidden"] = True
            self.fields["fecha_finaliza"].label = False

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_finaliza = cleaned_data.get("fecha_finaliza")
        if self.instance.tipo == 1:
            # Si servicio es eventual, fecha finaliza sera igual al inicio
            fecha_finaliza = fecha_inicio
        else:
            if fecha_inicio and fecha_finaliza:
                if fecha_inicio >= fecha_finaliza:
                    self.add_error(
                        "fecha_finaliza",
                        "La fecha de finalización no puede ser anterior o igual a la de fecha de inicio",
                    )
        if fecha_inicio < self.instance.fecha_emision:
            # Verificacion entre fecha de inicio y fecha de emision
            self.add_error(
                "fecha_inicio",
                "La fecha de inicio no puede ser anterior a la fecha de emisión",
            )
        return cleaned_data

    def save(self, commit=True):
        servicio = super().save(commit=False)
        if self.instance.tipo == 1:
            # Si servicio es eventual, se guarda la fecha de inicio en finalizacion
            servicio.fecha_finaliza = servicio.fecha_inicio
        if commit:
            servicio.save()
        return servicio


class FormAsignarEmpleados(forms.Form):
    frecuencia = forms.ModelChoiceField(
        label="Frecuencia",
        queryset=Frecuencia.objects.all(),
        widget=forms.Select(attrs={"class": "input"}),
    )
    empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.habilitados.all(),
        widget=forms.SelectMultiple(attrs={"class": "input"}),
        label="Empleados",
    )
