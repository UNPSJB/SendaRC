from django.shortcuts import render

# Create your views here.
def gestionServicios(request):
    return render(request, 'gestionServicios.html')

def presupuestar(request):
    return render(request, 'presupuestar.html')