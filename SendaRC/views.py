from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required 
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from .forms import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
            'form': AuthenticationForm
        })
    else:
        print(request.POST)