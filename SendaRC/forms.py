from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div,HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

# Login

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de Usuario', 
        widget=forms.TextInput(attrs={'class': 'input-login','placeholder': 'Ingrese su nombre de usuario'})
    )
    password = forms.CharField(
        label='Contraseña',  
        widget=forms.PasswordInput(attrs={'class': 'input-login','placeholder': 'Ingrese su contraseña'})
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField('username', css_class='input-login'),
                FloatingField('password', css_class='input-login'),
            )
        )

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de Usuario',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-login','placeholder': 'Ingrese su nombre de usuario'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'input-login','placeholder': 'Ingrese su email'})
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-login','placeholder': 'Ingrese su nombre'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-login','placeholder': 'Ingrese su apellido'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-login','placeholder': 'Ingrese su contraseña'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-login','placeholder': 'Confirme su contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField('username', css_class='input-login'),
                FloatingField('email', css_class='input-login'),
                FloatingField('first_name', css_class='input-login'),
                FloatingField('last_name', css_class='input-login'),
                FloatingField('password1', css_class='input-login'),
                FloatingField('password2', css_class='input-login'),
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar clase CSS al widget del campo de correo electrónico
        self.fields['email'].widget.attrs.update({'class': 'input-login','placeholder': 'Ingrese su correo electrónico'})

        # Agregar etiqueta personalizada al campo de correo electrónico
        self.fields['email'].label = 'Correo Electrónico'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField('email', css_class='input-login'),
            )
        )

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar clases CSS a los widgets
        self.fields['new_password1'].widget.attrs.update({'class': 'input-login','placeholder': 'Ingrese su nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'input-login','placeholder': 'Confirme su nueva contraseña'})

        # Agregar etiquetas personalizadas a los campos
        self.fields['new_password1'].label = 'Contraseña'
        self.fields['new_password2'].label = 'Confirmar Contraseña'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField('new_password1',css_class='input-login'),
                FloatingField('new_password2',css_class='input-login')
            )
        )

