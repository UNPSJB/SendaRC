from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings

class EmpleadoRestringidoMiddleware:
    """
    Middleware que restringe las vistas disponibles para los usuarios que pertenecen
    al grupo 'Empleado'. Los superusuarios tienen acceso total.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            nombre_vista = resolve(request.path_info).url_name
        except:
            nombre_vista = None

        # Si el usuario está autenticado...
        if request.user.is_authenticated:

            # Los superusuarios (admins) tienen acceso total
            if request.user.is_superuser:
                return self.get_response(request)

            # Si pertenece al grupo "Empleado"
            if request.user.groups.filter(name='Empleado').exists():
                # Vistas permitidas para los empleados
                vistas_permitidas_empleado = [
                    'calendario',
                    'home',
                    'eventos_calendario',
                    'debug_empleado',
                    'logout',
                ]

                if nombre_vista not in vistas_permitidas_empleado:
                    return redirect('home')

        return self.get_response(request)
