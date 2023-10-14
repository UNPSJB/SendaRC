from django.contrib import admin
from django.urls import path, include
from core.urls import * 
from SendaRC.views import *
from servicio.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name = 'home'),
    path('', login, name = 'login'),
    path('', include('core.urls')),
    path('', include('servicio.urls'))
]