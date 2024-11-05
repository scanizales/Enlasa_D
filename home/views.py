from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Project Tecnodesarrollo: Enlasa')

#vistas del apartado administrador
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

#vistas del apartado cliente
def principalCliente(request):
    return render(request, 'cliente/principal.html')

def miPerfil(request):
    return render(request, 'cliente/miPerfil.html')

def misPolizas(request):
    return render(request, 'cliente/misPolizas.html')

def misBeneficiarios(request):
    return render(request, 'cliente/misBeneficiarios.html')

#vistas del apartado gerente
def principalGerente(request):
    return render(request, 'gerente/principal.html')

def verPerfilGerente(request):
    return render(request, 'gerente/verPerfil.html')

def agregarAdministrador(request):
    return render(request, 'gerente/agregarAdministrador.html')

def verAdministradores(request):
    return render(request, 'gerente/verAdministradores.html')

def verEstadisticasGenerales(request):
    return render(request, 'gerente/verEstadisticasGenerales.html')

def verEstadisticasPorAseguradora(request):
    return render(request, 'gerente/verEstadisticasPorAseguradora.html')