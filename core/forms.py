from django import forms
from .models import *

class FormAltaInsumo(forms.ModelForm):
    incrementar = forms.BooleanField(required=False)
    class Meta:
        model = Insumo
        fields = ['descripcion', 'unidad_med', 'contenido_neto', 'marca', 'cantidad']
        widgets = {
            "descripcion": forms.Textarea(attrs={'class': 'form-control', 'cols': "12", 'rows': "10", "style": "min-height:100px"}),
            "unidad_med": forms.Select(attrs={'class': 'form-select'}),
            "contenido_neto": forms.NumberInput(attrs={'class': 'form-control'}),
            "marca": forms.TextInput(attrs={'class': 'form-control'}),
            "cantidad": forms.NumberInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        insumo = super().save(commit=commit)
        if self.cleaned_data['incrementar']:
            insumo.cantidad += 10
            insumo.save()
        return insumo