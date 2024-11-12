from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tipo_Seguro, Seguro

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
    if request.method == 'POST':
        nombre = request.POST.get('type')
        Tipo_Seguro.objects.create(nombre = nombre)       
        return redirect('admin_principal')
    
    return render(request, 'admin/agregarTipoSeguro.html')

def login(request):
    return render(request, 'public/iniciarSesion.html')

def agregarSeguro(request):
    tipos_seguros = Tipo_Seguro.objects.all()
    if request.method == 'POST':
        seguro = request.POST.get('type')
        tipo_seguro_id = int(request.POST.get('typeInsurance'))
        tipo_seguro = Tipo_Seguro.objects.get(id = tipo_seguro_id)
        Seguro.objects.create(nombre = seguro, tipo_seguro_id = tipo_seguro)
        return redirect('admin_principal')

    return render(request, 'admin/agregarSeguro.html',{
        'tipos_seguros': tipos_seguros
    })

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


def home(request):
    return render(request, 'layouts/basePublic.html')