from django import forms

class FormCobroFacturaSeña(forms.Form):
    formapago = forms.ChoiceField(choices=[(3, 'Transferencia'), (2, 'Cheque'), (1, 'Efectivo')])
