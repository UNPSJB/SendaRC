from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, HTML, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

# Login
"""
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login'}))
    

"""
class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                Div(
                    FloatingField('username'),
                    FloatingField('password'),
                    css_class='input-login'
                )
            )
        )

"""
class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email
"""

class RegisterForm(forms.Form):
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                Div(
                    FloatingField('username'),
                    FloatingField('email'),
                    FloatingField('password1'),
                    FloatingField('password2'),
                    css_class='input-login'
                )
            )
        )
