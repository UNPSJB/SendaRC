from django.contrib import admin
from django.urls import path, include,re_path
from core.urls import *
from .views import *
from .forms import *
from servicio.urls import *
from factura.urls import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),

    path('', include('core.urls')),
    path('servicio/', include('servicio.urls')),
    path('factura/', include('factura.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    re_path(r'^accounts/login/$', CustomLoginView, name='login'),
    path('', CustomLoginView, name='login'),
    path('logout/', logout, name='logout'),
    path('accounts/register/', register, name='register'),
    
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form_custom.html",
            form_class=CustomPasswordResetForm
        ), 
        name='password_reset'),
    
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done_custom.html",
        ), 
            name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm_custom.html",
            form_class=CustomSetPasswordForm
        ), 
        name='password_reset_confirm'),
    
    
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_complete_custom.html",
         ),
         name='password_reset_complete'),
]
