from django.contrib import admin
from django.urls import path, include
from core.urls import * 
from .views import *
from servicio.urls import *
from factura.urls import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name = 'home'),
    
    path('', include('core.urls')),
    path('servicio/', include('servicio.urls')),
    path('factura/', include('factura.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    #path('', login_required(Home.as_view()), name = 'home'),
    #path('login/', LoginView.as_view(), name='login'),
    #path('', LoginView.as_view(), name='login'),
    path('login/', login, name='login'),
    path('accounts/login/', login, name='login'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]