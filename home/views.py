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
    return render(request, 'admin/agregarSiniestros.html')

def verClientes(request):
    return render(request, 'admin/verClientes.html')

def verPolizas(request):
    return render(request, 'admin/verPolizas.html')

def verSiniestros(request):
    return render(request, 'admin/verSiniestros.html')

def agregarAseguradora(request):
    return render(request, 'admin/agregarAseguradora.html')

def verAseguradoras(request):
    return render(request, 'admin/verAseguradoras.html')

def agregarTipoSeguro(request):
    return render(request, 'admin/agregarTipoSeguro.html')

def agregarSeguro(request):
    return render(request, 'admin/agregarSeguro.html')

def verTiposSeguros(request):
    return render(request, 'admin/verTiposSeguros.html')

def verSeguros(request):
    return render(request, 'admin/verSeguros.html')
