from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def altaInsumo(request):
    return render(request, 'insumo/altaInsumo.html')