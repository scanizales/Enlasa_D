from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Tipo_Seguro, Seguro, Usuario, Aseguradora, Usuario, Cliente, Poliza, Beneficiario, Poliza_Beneficiario
from django.contrib.auth.hashers import make_password
import secrets
# configuración para enviar correo
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages

import random


def exit(request):
    logout(request)
    return redirect('home')

#vistas del apartado administrador
@login_required
def principalAdmin(request):
    return render(request, 'admin/principal.html')

@login_required
def verPerfil(request):
    return render(request, 'admin/verPerfil.html')

def agregarCliente(request):
    #inicializar datos de la modal
    modal = False
    mensaje = ''

    #obtener datos del form    
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

        try:
           cliente = Cliente.objects.get(num_documento = documento)
    
        except Cliente.DoesNotExist:
            Cliente.objects.create(
            nombre = nombre, num_documento = documento, tipo_documento = tipo_documento,
            celular = celular, email = email, ciudad = ciudad, telefono = telefono, direccion = direccion
            )
            #generar una contraseña
            cliente = Cliente.objects.get(num_documento = documento)
            def generar_contraseña():
               password = secrets.token_hex(4)
               return password

            #datos que se enviarán al correo 
            contraseña = generar_contraseña()    
            asunto = 'Contraseña de Enlasa'
            mensaje = f'Buen día señor(a) {nombre} su contraseña es: {contraseña}.\nLe recomendamos cambiarla.'
            remitente = settings.EMAIL_HOST_USER 
            destinatario = [email]

            #envío de la contraseña al correo
            send_mail(asunto, mensaje, remitente, destinatario)

            #creación de el usuario para el inicio de sesión  
            Usuario.objects.create(num_documento= documento, rol = 'CLIENTE',  nombre = nombre, email= email, password = make_password(contraseña))           
        
                
        #crear póliza
        Poliza.objects.create(fecha_inicio = fecha_inicio, fecha_vencimiento = fecha_vencimiento,
         valor = valor_prima, prima = tipo_prima, estado = estado, aseguradora_id = aseguradora, 
         seguro_id = seguro, cliente_id = cliente, medio_pago = medio_pago
        )

        #modal que comunica si el resgistro fue éxitoso
        modal = True
        mensaje = 'Póliza agregada con éxito.'

    #variables que van al template    
    context = {
        'seguros': Seguro.objects.all(),
        'aseguradoras': Aseguradora.objects.all(),
        'modal': modal,
        'mensaje': mensaje,
    }   

    return render(request, 'admin/agregarCliente.html',{
         'context': context       
    })

def agregarSiniestro(request):
    return render(request, 'admin/agregarSiniestros.html')

def verClientes(request):
    clients = Cliente.objects.all()
    if request.method == 'POST':
        type_document = request.POST.get('typeDocument')
        
        if type_document:
            clients = Cliente.objects.filter(tipo_documento = type_document)
            
    return render(request, 'admin/verClientes.html', {
        'clientes': clients
    })

def verPolizas(request):
    policys = Poliza.objects.all()
    context = {
        'insurances': Seguro.objects.all(),
        'insurers': Aseguradora.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
        'policys': policys,
    }  
    if request.method == 'POST':
        date_star = request.POST.get('startDate')
        date_end = request.POST.get('expiryDate')
        insurer = request.POST.get('insurer')
        insurance = request.POST.get('insurance')
        type_insurance = request.POST.get('type_insurance')
        state = request.POST.get('state')
        filters = {}
        if date_star:
            filters['fecha_inicio'] = date_star

        if date_end:
            filters['fecha_vencimiento'] = date_end

        if insurer and not "":
            filters['aseguradora_id'] = insurer

        if insurance and not "":
            filters['seguro_id'] = insurance

        if type_insurance and not "":
            filters['seguro_id__tipo_seguro_id'] = type_insurance

        if state and not "":
            filters['estado'] = state
            
        policys = Poliza.objects.filter(**filters)
        context['policys'] = policys

    return render(request, 'admin/verPolizas.html',{
         'context': context       
    })

def verSiniestros(request):
    context = {
        'insurers': Aseguradora.objects.all(),
        'insurances': Seguro.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
    } 

    return render(request, 'admin/verSiniestros.html',{
        'context': context       
    })

def agregarAseguradora(request):
    modal = False
    mensaje = ''
    if request.method == 'POST':
        nombre = request.POST.get('name')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
        Aseguradora.objects.create(nombre = nombre, telefono = telefono, direccion = direccion)
        modal = True
        mensaje = f'La aseguradora {nombre} ha sido agregada.'
    
    context = {
        'modal': modal,
        'mensaje': mensaje,
    } 

    return render(request, 'admin/agregarAseguradora.html',{
         'context': context       
    })


def verAseguradoras(request):
    aseguradoras = Aseguradora.objects.all()
    return render(request, 'admin/verAseguradoras.html', {
        'aseguradoras':aseguradoras
    })

def agregarTipoSeguro(request):
    modal = False
    mensaje = ''
    if request.method == 'POST':
        nombre = request.POST.get('type')
        Tipo_Seguro.objects.create(nombre = nombre)       
        modal = True
        mensaje = f'El tipo de seguro:  {nombre}, ha sido agregado.'
    
    context = {
    'modal': modal,
    'mensaje': mensaje,
    } 

    return render(request, 'admin/agregarTipoSeguro.html',{
         'context': context       
    })

def iniciar_sesion(request):
    if request.method == 'POST':
        documento = request.POST.get('numDocument')
        contraseña = request.POST.get('password')
        usuario = authenticate(num_documento = documento, password = contraseña)
        if usuario is not None:
            login(request, usuario)
            if usuario.rol == settings.ROLE_CLIENTE:
               redirect_url = settings.ROLE_REDIRECT_URLS.get(usuario.rol) 
               return redirect(redirect_url)

            elif usuario.rol == settings.ROLE_ADMINISTRADOR:
                redirect_url = settings.ROLE_REDIRECT_URLS.get(usuario.rol)
                return redirect(redirect_url)

            else:
                redirect_url == settings.ROLE_REDIRECT_URLS.get('GERENTE')
                return redirect(redirect_url )
        else:
            return HttpResponse('No se encuentra su usuario')  

    return render(request, 'public/iniciarSesion.html')

def agregarSeguro(request):
    modal = False
    mensaje = ''
    tipos_seguros = Tipo_Seguro.objects.all()
    if request.method == 'POST':
        seguro = request.POST.get('type')
        tipo_seguro_id = int(request.POST.get('typeInsurance'))
        tipo_seguro = Tipo_Seguro.objects.get(id = tipo_seguro_id)
        Seguro.objects.create(nombre = seguro, tipo_seguro_id = tipo_seguro)
        modal = True
        mensaje = f'El seguro: {seguro}, ha sido agregado.'

    context = {
    'modal': modal,
    'mensaje': mensaje,
    'tipos_seguros': tipos_seguros,
    } 

    return render(request, 'admin/agregarSeguro.html',{
         'context': context       
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
@login_required
def principalCliente(request):
    return render(request, 'cliente/principal.html')

def miPerfil(request):
    documento = request.user.num_documento
    cliente = Cliente.objects.get(num_documento = documento)
    
    return render(request, 'cliente/miPerfil.html', {
        'cliente': cliente
    })
    return render(request, 'cliente/miPerfil.html')

def misPolizas(request):
    documento = request.user.num_documento
    cliente = Cliente.objects.get(num_documento = documento)
    policys_all = Poliza.objects.filter(cliente_id = cliente)
    context = {
        'insurers': Aseguradora.objects.all(),
        'insurances': Seguro.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
        'policys': policys_all,
    } 
    if request.method == 'POST':
        date_star = request.POST.get('startDate')
        date_end = request.POST.get('expiryDate')
        insurer = request.POST.get('insurer')
        insurance = request.POST.get('insurance')
        type_insurance = request.POST.get('type_insurance')
        state = request.POST.get('state')
        filters = {}
        if date_star:
            filters['fecha_inicio'] = date_star

        if date_end:
            filters['fecha_vencimiento'] = date_end

        if insurer and not "":
            filters['aseguradora_id'] = insurer

        if insurance and not "":
            filters['seguro_id'] = insurance

        if type_insurance and not "":
            filters['seguro_id__tipo_seguro_id'] = type_insurance

        if state and not "":
            filters['estado'] = state
            
        policys = policys_all.filter(**filters)
        context['policys'] = policys

    return render(request, 'cliente/misPolizas.html',{
        'context': context       
    })


def misBeneficiarios(request):
    return render(request, 'cliente/misBeneficiarios.html')

#vistas del apartado gerente

def principalGerente(request):
    return render(request, 'gerente/principal.html')

def verPerfilGerente(request):
    return render(request, 'gerente/verPerfil.html')

def agregarAdministrador(request):
    modal = False
    mensaje = ''
    if request.method == 'POST':
        nombre = request.POST.get('name')

        def generar_usuario():
            return random.sample(range(10), 8)   

        numero = generar_usuario()
        usuario = int("".join(map(str, numero)))
      
        email = request.POST.get('email')
        password = request.POST.get('password')
        Usuario.objects.create(num_documento= usuario, rol = 'ADMINISTRADOR',  nombre = nombre, email= email, password = make_password(password))       
        modal = True
        mensaje = f'Se ha agregado a {nombre} como administrador.'
    
    context = {
    'modal': modal,
    'mensaje': mensaje,
    } 

    return render(request, 'gerente/agregarAdministrador.html',{
         'context': context       
    })

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

def edit_insurer(request, insurer_id):
    insurer = Aseguradora.objects.get(id = insurer_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        insurer.nombre = name
        insurer.telefono = phone
        insurer.direccion = address
        insurer.save()
        modal = True
        message = 'Se realizaron los cambios exitosamente.'
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
 
    context = {
    'modal': modal,
    'message': message,
    'insurer': insurer
    } 

    return render(request, 'admin/editInsurer.html',{
         'context': context       
    }) 

def add_beneficiary(request, policy_id):
    
    policy = Poliza.objects.get(id = policy_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')

        Beneficiario.objects.create(num_documento= document, nombre = name, tipo_documento = type_document)
        beneficiary = Beneficiario.objects.get(num_documento = document)
        if beneficiary:
           Poliza_Beneficiario.create(poliza_id = policy, beneficiario_id = beneficiary) 
           message = f'La persona {name} fue agregado como beneficario a la póliza {policy.seguro_id.nombre} a cargo de señor(a) {policy.cliente_id.nombre}'
        
        else:
            message = 'No se pudo agregar el beneficiario'
   
    context = {
    'modal': modal,
    'message': message,
    } 

    return render(request, 'admin/addBeneficiary.html',{
         'context': context       
    })

#Public

def nosotros(request):
    return render(request, 'public/nosotros.html')

def segurosGenerales(request):
    return render(request, 'public/segurosGenerales.html')

def segurosHogar(request):
    return render(request, 'public/segurosHogar.html')

def home(request):
    return render(request, 'layouts/basePublic.html')