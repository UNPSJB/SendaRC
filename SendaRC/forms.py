from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from crispy_bootstrap5.bootstrap5 import FloatingField
# Login
class CustomAuthenticationForm(AuthenticationForm):
    #username = forms.CharField(
    #    widget=forms.TextInput(attrs={'class': 'input-login'}),
    #)
    #password = forms.CharField(
    #    widget=forms.PasswordInput(attrs={'class': 'input-login'}),
    #)
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
    
    #class Meta:
     #   widgets={'username': }

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