from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout, login as auth_login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here
@login_required
def home(request):
    request.session['presupuesto'] = {}
    request.session['servicios'] = []
    request.session['frecuencias'] = []
    return render(request, 'home.html')

def CustomLoginView(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {"form": LoginForm()})
    else:
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            form.add_error('username', 'Usuario o contraseña incorrectos. Por favor, intenta nuevamente.')
        return render(request, 'registration/login.html', {"form": form})
        
@login_required
def logout(request):
    django_logout(request)
    return redirect('login')

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {"form": RegisterForm})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                    user.save()
                    return redirect('login')
                except IntegrityError:
                    form.add_error('username', 'Usuario ya existe')
            else:
                form.add_error('password2', 'Las contraseñas no coinciden')

        return render(request, 'registration/register.html', {"form": form})

