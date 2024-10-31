from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Project Tecnodesarrollo: Enlasa')

def principalAdmin(request):
    return render(request, 'admin/principal.html')

def verPerfil(request):
    return render(request, 'admin/verPerfil.html')

def agregarCliente(request):
    return render(request, 'admin/agregarCliente.html')

def agregarSiniestro(request):
    return render(request, 'admin/agregarSiniestro.html')

def verClientes(request):
    return render(request, 'admin/verClientes.html')