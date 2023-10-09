from django import forms
from .models import *

class FormAltaInsumo(forms.ModelForm):
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
        super(FormAltaInsumo, self).__init__(*args, **kwargs)
        # Oculta las etiquetas de los campos
        self.fields['descripcion'].label = False
        self.fields['unidad_med'].label = False
        self.fields['contenido_neto'].label = False
        self.fields['marca'].label = False
        self.fields['cantidad'].label = False

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cuil','nombre', 'apellido', 'direccion', 'tipo', 'tipoPersona','telefono','email','localidad']
        widgets = {
            "cuil": forms.NumberInput(attrs={'class': 'form-control textarea','placeholder':'CUIL/CUIT'}),
            "nombre": forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre'}),
            "apellido": forms.TextInput(attrs={'class': 'form-control','placeholder':'Apellido'}),
            "direccion": forms.TextInput(attrs={'class': 'form-control','placeholder':'Dirección'}),
            "telefono": forms.NumberInput(attrs={'class': 'form-control','placeholder':'Telefono'}),
            "email": forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
            "tipo": forms.Select(attrs={'class': 'form-select','placeholder':'Tipo cliente'}),
            "tipoPersona": forms.Select(attrs={'class': 'form-select','placeholder':'Tipo persona'}),
            "localidad": forms.TextInput(attrs={'class': 'form-control','placeholder':'Localidad'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        # Oculta las etiquetas de los campos
        self.fields['cuil'].label = False
        self.fields['nombre'].label = False
        self.fields['apellido'].label = False
        self.fields['direccion'].label = False
        self.fields['tipo'].label = False
        self.fields['tipoPersona'].label = False
        self.fields['telefono'].label = False
        self.fields['email'].label = False
        self.fields['localidad'].label = False