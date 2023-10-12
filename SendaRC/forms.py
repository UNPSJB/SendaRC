from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_bootstrap5.bootstrap5 import FloatingField
# Login
class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-login'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-login'}),
    )
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
