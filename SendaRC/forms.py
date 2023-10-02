from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Login
class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Usuario'}),
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Contraseña'}),
    )

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Oculta las etiquetas de los campos
        self.fields['username'].label = False
        self.fields['password'].label = False
