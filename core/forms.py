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
        fields = ["tipo", "nroSancion", "empleado"]

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        if is_modificar:
            mensaje = "Modificar una sancion aquí. Dale click en guardar al terminar"
        else:
            mensaje = "Agregar una sancion aquí. Dale click en guardar al terminar"
        super(FormSancion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<p class="info-formulario">{}</p>'.format(mensaje)),
                Fieldset(
                    Div(),
                    Div(
                        FloatingField("tipo"),
                        FloatingField("nroSancion"),
                        FloatingField("empleado"),
                        css_class="container-inputs-form",
                    ),
                ),
                Div(
                    HTML(
                        '<a href="{% url "gestionSanciones" %}" class="btn-Cancelar">Cancelar</a>'
                    ),
                    Submit("submit", "Guardar", css_class="btn-Guardar"),
                    css_class="input-group mb-3 operaciones",
                ),
                css_class="container-forms",
            )
        )


class FormEmpleado(forms.ModelForm):
    numDNI = ARDNIField(label="DNI", error_messages={"invalid": "DNI no válido"})

    class Meta:
        model = Empleado
        fields = [
            "numDNI",
            "nombre",
            "apellido",
            "telefono",
            "email",
            "sueldo",
            "localidad",
            "activo",
        ]
        widgets = {
            "numDNI": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "sueldo": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "localidad": forms.Select(attrs={"class": "form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Si estamos modificando, hay que excluir el propio empleado
        empleado_id = self.instance.pk
        if User.objects.filter(email=email).exclude(empleado__pk=empleado_id).exists():
            raise forms.ValidationError("Este email ya está en uso.")
        return email

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super().__init__(*args, **kwargs)

        if is_modificar:
            mensaje = (
                "Actualice los datos del empleado y haga clic en 'Guardar Empleado'"
            )
        else:
            mensaje = "Complete los datos del nuevo empleado y haga clic en 'Guardar Empleado'"

        self.fields["localidad"].queryset = Localidad.objects.all()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                # DNI
                Div(
                    HTML(
                        """
                        <label for="{{ form.numDNI.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            DNI
                        </label>
                        """
                    ),
                    Field("numDNI", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Nombre
                Div(
                    HTML(
                        """
                        <label for="{{ form.nombre.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Nombre
                        </label>
                        """
                    ),
                    Field("nombre", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Apellido
                Div(
                    HTML(
                        """
                        <label for="{{ form.apellido.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Apellido
                        </label>
                        """
                    ),
                    Field("apellido", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Teléfono
                Div(
                    HTML(
                        """
                        <label for="{{ form.telefono.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                            </svg>
                            Teléfono
                        </label>
                        """
                    ),
                    Field("telefono", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Email
                Div(
                    HTML(
                        """
                        <label for="{{ form.email.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                <polyline points="22,6 12,13 2,6"></polyline>
                            </svg>
                            Email
                        </label>
                        """
                    ),
                    Field("email", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Sueldo
                Div(
                    HTML(
                        """
                        <label for="{{ form.sueldo.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <line x1="12" y1="1" x2="12" y2="23"></line>
                                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Sueldo
                        </label>
                        """
                    ),
                    Field("sueldo", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Localidad
                Div(
                    HTML(
                        """
                        <label for="{{ form.localidad.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            Localidad
                        </label>
                        """
                    ),
                    Field("localidad", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Activo
                Div(
                    Div(
                        Field(
                            "activo",
                            wrapper_class="form-check",
                            css_class="form-check-input",
                        ),
                        HTML(
                            '<label class="form-check-label" for="{{ form.activo.id_for_label }}">Empleado activo</label>'
                        ),
                        css_class="form-check",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionEmpleado\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit("submit", "Guardar Empleado", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class FormLocalidad(forms.ModelForm):
    cp = ARPostalCodeField(
        label="Código Postal", error_messages={"invalid": "Código postal no válido"}
    )

    class Meta:
        model = Localidad
        fields = ["cp", "nombre"]
        widgets = {
            "cp": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super().__init__(*args, **kwargs)

        if is_modificar:
            mensaje = (
                "Actualice los datos de la localidad y haga clic en 'Guardar Localidad'"
            )
        else:
            mensaje = "Complete los datos de la nueva localidad y haga clic en 'Guardar Localidad'"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                # Código Postal
                Div(
                    HTML(
                        """
                        <label for="{{ form.cp.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                <polyline points="22,6 12,13 2,6"></polyline>
                            </svg>
                            Código Postal
                        </label>
                        """
                    ),
                    Field("cp", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Nombre
                Div(
                    HTML(
                        """
                        <label for="{{ form.nombre.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Nombre
                        </label>
                        """
                    ),
                    Field("nombre", wrapper_class=""),
                    css_class="col-md-6",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionLocalidad\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit("submit", "Guardar Localidad", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class FormInsumo(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = [
            "descripcion",
            "unidad_med",
            "contenido_neto",
            "marca",
            "cantidad",
            "activo",
        ]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "unidad_med": forms.Select(attrs={"class": "form-select"}),
            "contenido_neto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super().__init__(*args, **kwargs)

        if is_modificar:
            mensaje = "Actualice los datos del insumo y haga clic en 'Guardar Insumo'"
        else:
            mensaje = (
                "Complete los datos del nuevo insumo y haga clic en 'Guardar Insumo'"
            )

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                # Descripción
                Div(
                    HTML(
                        """
                        <label for="{{ form.descripcion.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <rect x="1" y="3" width="15" height="13"></rect>
                                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                                <circle cx="18.5" cy="18.5" r="2.5"></circle>
                            </svg>
                            Descripción
                        </label>
                        """
                    ),
                    Field("descripcion", wrapper_class=""),
                    css_class="col-md-12",
                ),
                # Unidad de Medida
                Div(
                    HTML(
                        """
                        <label for="{{ form.unidad_med.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Unidad de Medida
                        </label>
                        """
                    ),
                    Field("unidad_med", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Contenido Neto
                Div(
                    HTML(
                        """
                        <label for="{{ form.contenido_neto.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <line x1="12" y1="1" x2="12" y2="23"></line>
                                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Contenido Neto
                        </label>
                        """
                    ),
                    Field("contenido_neto", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Marca
                Div(
                    HTML(
                        """
                        <label for="{{ form.marca.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                                <line x1="12" y1="22.08" x2="12" y2="12"></line>
                            </svg>
                            Marca
                        </label>
                        """
                    ),
                    Field("marca", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Cantidad
                Div(
                    HTML(
                        """
                        <label for="{{ form.cantidad.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Cantidad
                        </label>
                        """
                    ),
                    Field("cantidad", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Activo
                Div(
                    Div(
                        Field(
                            "activo",
                            wrapper_class="form-check",
                            css_class="form-check-input",
                        ),
                        HTML(
                            '<label class="form-check-label" for="{{ form.activo.id_for_label }}">Insumo activo</label>'
                        ),
                        css_class="form-check",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionInsumos\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit("submit", "Guardar Insumo", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class ClienteForm(forms.ModelForm):
    cuil = ARCUITField(label="CUIL", error_messages={"invalid": "CUIL no válido"})

    class Meta:
        model = Cliente
        fields = [
            "cuil",
            "nombre",
            "apellido",
            "direccion",
            "tipo",
            "tipoPersona",
            "telefono",
            "email",
            "localidad",
            "activo",
        ]
        widgets = {
            "cuil": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "tipoPersona": forms.Select(attrs={"class": "form-select"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "localidad": forms.Select(attrs={"class": "form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super().__init__(*args, **kwargs)

        if is_modificar:
            mensaje = "Actualice los datos del cliente y haga clic en 'Guardar Cliente'"
        else:
            mensaje = (
                "Complete los datos del nuevo cliente y haga clic en 'Guardar Cliente'"
            )

        self.fields["localidad"].queryset = Localidad.objects.all()
        self.fields["tipo"].widget.attrs["hidden"] = not is_modificar

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False  # evita labels duplicados

        self.helper.layout = Layout(
            Div(
                # CUIL
                Div(
                    HTML(
                        """
                        <label for="{{ form.cuil.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            CUIT / CUIL
                        </label>
                        """
                    ),
                    Field("cuil", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Nombre
                Div(
                    HTML(
                        """
                        <label for="{{ form.nombre.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Nombre
                        </label>
                        """
                    ),
                    Field("nombre", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Apellido
                Div(
                    HTML(
                        """
                        <label for="{{ form.apellido.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Apellido
                        </label>
                        """
                    ),
                    Field("apellido", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Dirección
                Div(
                    HTML(
                        """
                        <label for="{{ form.direccion.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            Dirección
                        </label>
                        """
                    ),
                    Field("direccion", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Localidad
                Div(
                    HTML(
                        """
                        <label for="{{ form.localidad.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            Localidad
                        </label>
                        """
                    ),
                    Field("localidad", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Teléfono
                Div(
                    HTML(
                        """
                        <label for="{{ form.telefono.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                            </svg>
                            Teléfono
                        </label>
                        """
                    ),
                    Field("telefono", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Email
                Div(
                    HTML(
                        """
                        <label for="{{ form.email.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                <polyline points="22,6 12,13 2,6"></polyline>
                            </svg>
                            Email
                        </label>
                        """
                    ),
                    Field("email", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Tipo Cliente
                Div(
                    HTML(
                        """
                        <label for="{{ form.tipo.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                            </svg>
                            Tipo Cliente
                        </label>
                        """
                    ),
                    Field("tipo", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Tipo Persona
                Div(
                    HTML(
                        """
                        <label for="{{ form.tipoPersona.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                            </svg>
                            Tipo Persona
                        </label>
                        """
                    ),
                    Field("tipoPersona", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Activo
                Div(
                    Div(
                        Field(
                            "activo",
                            wrapper_class="form-check",
                            css_class="form-check-input",
                        ),
                        HTML(
                            '<label class="form-check-label" for="{{ form.activo.id_for_label }}">Cliente activo</label>'
                        ),
                        css_class="form-check",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionClientes\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit("submit", "Guardar Cliente", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = [
            "descripcion",
            "unidad_medida",
            "precio",
            "insumos",
            "maquinarias",
            "activo",
        ]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "unidad_medida": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "insumos": forms.SelectMultiple(attrs={"class": "form-select"}),
            "maquinarias": forms.SelectMultiple(attrs={"class": "form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super(TipoServicioForm, self).__init__(*args, **kwargs)

        if is_modificar:
            mensaje = "Agregue los nuevos datos del tipo de servicio. Dale click en guardar al terminar"
        else:
            mensaje = "Agrega los datos de un nuevo tipo de servicio. Dale click en guardar al terminar"

        self.fields["insumos"].queryset = Insumo.habilitados.all()
        self.fields["maquinarias"].queryset = Maquinaria.objects.all()
        self.fields["maquinarias"].required = False

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False  # Importante para evitar labels duplicados

        self.helper.layout = Layout(
            Div(
                # Descripción
                Div(
                    HTML(
                        """
                        <label for="{{ form.descripcion.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <rect x="1" y="3" width="15" height="13"></rect>
                                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                                <circle cx="18.5" cy="18.5" r="2.5"></circle>
                            </svg>
                            Descripción
                        </label>
                    """
                    ),
                    Field("descripcion", wrapper_class=""),
                    css_class="col-md-12",
                ),
                # Unidad de Medida
                Div(
                    HTML(
                        """
                        <label for="{{ form.unidad_medida.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Unidad de Medida
                        </label>
                    """
                    ),
                    Field("unidad_medida", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Precio
                Div(
                    HTML(
                        """
                        <label for="{{ form.precio.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <line x1="12" y1="1" x2="12" y2="23"></line>
                                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Precio
                        </label>
                    """
                    ),
                    Field("precio", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Insumos
                Div(
                    HTML(
                        """
                        <label for="{{ form.insumos.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                                <line x1="12" y1="22.08" x2="12" y2="12"></line>
                            </svg>
                            Insumos Necesarios
                        </label>
                    """
                    ),
                    Field("insumos", wrapper_class=""),
                    HTML(
                        '<div class="form-text">Seleccione los insumos necesarios para este tipo de servicio</div>'
                    ),
                    css_class="col-md-12",
                ),
                # Maquinarias
                Div(
                    HTML(
                        """
                        <label for="{{ form.maquinarias.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
                            </svg>
                            Maquinarias Necesarias
                        </label>
                    """
                    ),
                    Field("maquinarias", wrapper_class=""),
                    HTML(
                        '<div class="form-text">Seleccione las maquinarias necesarias para este tipo de servicio</div>'
                    ),
                    css_class="col-md-12",
                ),
                # Activo
                Div(
                    Div(
                        Field(
                            "activo",
                            wrapper_class="form-check",
                            css_class="form-check-input",
                        ),
                        HTML(
                            '<label class="form-check-label" for="{{ form.activo.id_for_label }}">Tipo de servicio activo</label>'
                        ),
                        css_class="form-check",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionTipoServicio\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit(
                    "submit", "Guardar Tipo de Servicio", css_class="btn btn-primary"
                ),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class FormAltaMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ["nombre", "modelo", "marca", "cantidad", "activo", "observaciones"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        is_modificar = kwargs.pop("is_modificar", False)
        super().__init__(*args, **kwargs)

        if is_modificar:
            mensaje = "Actualice los datos de la maquinaria y haga clic en 'Guardar Maquinaria'"
        else:
            mensaje = "Complete los datos de la nueva maquinaria y haga clic en 'Guardar Maquinaria'"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}
        self.helper.form_show_labels = False  # evita labels duplicados

        self.helper.layout = Layout(
            Div(
                # Nombre
                Div(
                    HTML(
                        """
                        <label for="{{ form.nombre.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            Nombre
                        </label>
                        """
                    ),
                    Field("nombre", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Modelo
                Div(
                    HTML(
                        """
                        <label for="{{ form.modelo.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                            </svg>
                            Modelo
                        </label>
                        """
                    ),
                    Field("modelo", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Marca
                Div(
                    HTML(
                        """
                        <label for="{{ form.marca.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                            </svg>
                            Marca
                        </label>
                        """
                    ),
                    Field("marca", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Cantidad
                Div(
                    HTML(
                        """
                        <label for="{{ form.cantidad.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                            Cantidad
                        </label>
                        """
                    ),
                    Field("cantidad", wrapper_class=""),
                    css_class="col-md-6",
                ),
                # Observaciones
                Div(
                    HTML(
                        """
                        <label for="{{ form.observaciones.id_for_label }}" class="form-label">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;">
                                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
                            </svg>
                            Observaciones
                        </label>
                        """
                    ),
                    Field("observaciones", wrapper_class=""),
                    css_class="col-md-12",
                ),
                # Activo
                Div(
                    Div(
                        Field(
                            "activo",
                            wrapper_class="form-check",
                            css_class="form-check-input",
                        ),
                        HTML(
                            '<label class="form-check-label" for="{{ form.activo.id_for_label }}">Maquinaria activa</label>'
                        ),
                        css_class="form-check",
                    ),
                    css_class="col-md-12",
                ),
                css_class="row g-3",
            ),
            # Botones
            Div(
                HTML(
                    '<a href="{% url \'gestionMaquinaria\' %}" class="btn btn-secondary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg> Cancelar</a>'
                ),
                Submit("submit", "Guardar Maquinaria", css_class="btn btn-primary"),
                css_class="d-flex gap-2 justify-content-end mt-4",
            ),
        )


class FiltroClientesForm(forms.Form):
    ESTADOS = [("Activos", "Activos"), ("No activos", "No activos"), ("Todos", "Todos")]
    TIPOS_PERSONA = [("", "---"), ("1", "Particular"), ("2", "Jurídico")]
    TIPOS = [("", "---"), ("1", "Ocasional"), ("2", "Habitual")]

    estado = forms.ChoiceField(choices=ESTADOS, required=False)
    tipo_persona = forms.ChoiceField(choices=TIPOS_PERSONA, required=False)
    tipo = forms.ChoiceField(choices=TIPOS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "w-100"
        self.helper.layout = Layout(
            Div(
                Div(Field("estado", css_class="form-select form-select-sm form-select-filter"), css_class="col-12 col-md"),
                Div(Field("tipo_persona", css_class="form-select form-select-sm form-select-filter"), css_class="col-12 col-md"),
                Div(Field("tipo", css_class="form-select form-select-sm form-select-filter"), css_class="col-12 col-md"),
                css_class="row g-2"
            )
        )



class FiltroActivoForm(forms.Form):
    ESTADOS = [("Activos", "Activos"), ("No activos", "No activos"), ("Todos", "Todos")]

    estado = forms.ChoiceField(choices=ESTADOS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "w-100"
        self.helper.layout = Layout(
            Div(
                Div(Field("estado", css_class="form-select form-select-sm form-select-filter"), css_class="col-12 col-md-6"),
                css_class="row g-2"
            )
        )

