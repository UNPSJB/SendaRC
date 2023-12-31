from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required 
from django.contrib import messages
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here
@login_required
def home(request):
    request.session['presupuesto'] = {}
    request.session['servicios'] = []
    request.session['frecuencias'] = []
    return render(request, 'home.html')

def login(request):
    data = {
        'form': LoginForm()
    }
    if request.method == 'POST':
        user_creation_form = LoginForm(data=request.POST)
        if user_creation_form.is_valid():
            username = user_creation_form.cleaned_data['username']
            password = user_creation_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                #user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password'])
                django_login(request, user)
                return redirect('home')
            else:
                print("Login Invalido")            
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/login.html', data)
        
@login_required
def logout(request):
    django_logout(request)
    return redirect('login')

def register(request):
    # Form por defecto de Django para poder crear un registro 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario_new = User.objects.create(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                # Logeamos el usuario 
            usuario_new.save()
            # Autenticamos el usuario
            print("-----------MOSTRAMOS SI ENTRA A POST", form.cleaned_data)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                print("-----------MOSTRAMOS SI AUTENTICA", form.cleaned_data)
                
                username = form.cleaned_data['username']
                messages.success(request, f'Usuario {username} creado')
                django_login(request, user)
            else:
                print("Login Invalido")
            
            return redirect('home')
        else:
            print(form.errors)

    form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

"""
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            django_login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)
"""
"""
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Llama al método login para autenticar al usuario
            django_login(self.request, user)
            return super().form_valid(form)
        else:
            # El usuario no está autenticado, maneja el error según tus necesidades
            return self.form_invalid(form)
"""