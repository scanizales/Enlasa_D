from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Tipo_Seguro, Seguro, Usuario, Aseguradora, Usuario, Cliente, Poliza
from django.contrib.auth.hashers import make_password

def home(request):
    return HttpResponse('Project Tecnodesarrollo: Enlasa')

#vistas del apartado administrador
def principalAdmin(request):
    return render(request, 'admin/principal.html')

def verPerfil(request):
    return render(request, 'admin/verPerfil.html')

def agregarCliente(request):
    if request.method == 'POST':
        #datos de cliente
        nombre = request.POST.get('name')
        tipo_documento = request.POST.get('typeDocument')
        documento = request.POST.get('document')
        celular = request.POST.get('phone')
        telefono = request.POST.get('phone2')
        email = request.POST.get('email')
        ciudad = request.POST.get('city')
        direccion = request.POST.get('address')
        #datos de póliza
        estado = request.POST.get('state')
        fecha_inicio = request.POST.get('startDate')
        fecha_vencimiento = request.POST.get('expiryDate') 
        tipo_prima = request.POST.get('typeFace') 
        valor_prima = request.POST.get('valueFace') 
        medio_pago = request.POST.get('payMethod') 
        aseguradora_id  = request.POST.get('insurer')
        seguro_id = request.POST.get('insurance')
        seguro = Seguro.objects.get(id = seguro_id)
        aseguradora = Aseguradora.objects.get(id = aseguradora_id)
        #crear cliente
        cliente, created = Cliente.objects.get_or_create(
            nombre = nombre, num_documento = documento, tipo_documento = tipo_documento,
            celular = celular, email = email, ciudad = ciudad, telefono = telefono, direccion = direccion
        )       
        #crear póliza
        Poliza.objects.create(fecha_inicio = fecha_inicio, fecha_vencimiento = fecha_vencimiento,
         valor = valor_prima, prima = tipo_prima, estado = estado, aseguradora_id = aseguradora, 
         seguro_id = seguro, cliente_id = cliente, medio_pago = medio_pago
        )
        return render(request, 'admin/principal.html')
        
 
    context = {
        'seguros': Seguro.objects.all(),
        'aseguradoras': Aseguradora.objects.all()
    }   

    return render(request, 'admin/agregarCliente.html',{
         'context': context
    })

def agregarSiniestro(request):
    return render(request, 'admin/agregarSiniestros.html')

def verClientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'admin/verClientes.html', {
        'clientes': clientes
    })

def verPolizas(request):
    polizas = Poliza.objects.all()
    return render(request, 'admin/verPolizas.html', {
        'polizas': polizas
    })

def verSiniestros(request):
    return render(request, 'admin/verSiniestros.html')

def agregarAseguradora(request):
    if request.method == 'POST':
        nombre = request.POST.get('name')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
        Aseguradora.objects.create(nombre = nombre, telefono = telefono, direccion = direccion)
        return redirect('admin_principal')

    return render(request, 'admin/agregarAseguradora.html')

def verAseguradoras(request):
    aseguradoras = Aseguradora.objects.all()
    return render(request, 'admin/verAseguradoras.html', {
        'aseguradoras':aseguradoras
    })

def agregarTipoSeguro(request):
    if request.method == 'POST':
        nombre = request.POST.get('type')
        Tipo_Seguro.objects.create(nombre = nombre)       
        return redirect('admin_principal')
    
    return render(request, 'admin/agregarTipoSeguro.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        tipo_documento = request.POST.get('typeDocument')
        documento = request.POST.get('numDocument')
        contraseña = request.POST.get('password')
        usuario = authenticate(tipo_documento = tipo_documento, num_documento = documento, password = contraseña)
        if usuario is not None:
            login(request, usuario)
            if usuario.rol == 'CLIENTE':
                return redirect('cliente_principal')

            elif usuario.rol == 'ADMINISTRADOR':
                return redirect('admin_principal')
            else:
                return redirect('gerente_principal')
        else:
            return HttpResponse('No se encuentra su usuario')   
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
    tipos_seguros = Tipo_Seguro.objects.all()
    return render(request, 'admin/verTiposSeguros.html', {
        'tipos_seguros':tipos_seguros
    })   

def verSeguros(request):
    seguros = Seguro.objects.all()
    return render(request, 'admin/verSeguros.html', {
        'seguros': seguros
    })  


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
    if request.method == 'POST':
        nombre = request.POST.get('name')
        tipo_documento = request.POST.get('typeDocument')
        documento = request.POST.get('document')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Usuario.objects.create(num_documento= documento, tipo_documento =tipo_documento, rol = 'ADMINISTRADOR',  nombre = nombre, email= email, password = make_password(password))       
        return redirect('admin_principal')

    return render(request, 'gerente/agregarAdministrador.html')

def verAdministradores(request):
    usuarios = Usuario.objects.all()
    administradores = []
    for usuario in usuarios:
        if usuario.rol == 'ADMINISTRADOR':
            administradores.append(usuario)
         
    return render(request, 'gerente/verAdministradores.html', {
        'administradores': administradores
    })  

def verEstadisticasGenerales(request):
    return render(request, 'gerente/verEstadisticasGenerales.html')

def verEstadisticasPorAseguradora(request):
    return render(request, 'gerente/verEstadisticasPorAseguradora.html')


def home(request):
    return render(request, 'layouts/basePublic.html')


#Public

def nosotros(request):
    return render(request, 'public/nosotros.html')

def segurosGenerales(request):
    return render(request, 'public/segurosGenerales.html')

def segurosHogar(request):
    return render(request, 'public/segurosHogar.html')