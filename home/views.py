from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Tipo_Seguro, Seguro, Usuario, Aseguradora, Usuario, Cliente, Poliza, Beneficiario, Policy_Beneficiary, Siniestro
from django.contrib.auth.hashers import make_password
import secrets
# configuración para enviar correo
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages
from datetime import date
import random

def exit(request):
    logout(request)
    return redirect('home')

#vistas del apartado administrador
@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

@login_required
def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

def create_client_policy(request):
    #inicializar datos de la modal
    modal = False
    message_modal = ''

    #obtener datos del form    
    if request.method == 'POST':

        #datos de cliente
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')
        phone_mobile = request.POST.get('phone')
        phone = request.POST.get('phone2')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')

        #datos de póliza
        state = request.POST.get('state')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('expiryDate') 
        type_premium = request.POST.get('typeFace') 
        value_premium = request.POST.get('valueFace') 
        payment_method = request.POST.get('payMethod') 
        insurer_id  = request.POST.get('insurer')
        insurance_id = request.POST.get('insurance')

        #obtener las onstancias de aseguradora y seguro
        insurer = Aseguradora.objects.get(id = insurer_id)
        insurance = Seguro.objects.get(id = insurance_id)

        #validar si el cliente existe
        try:
           client = Cliente.objects.get(num_documento = document)


        #sino existe se crea el cliente y el usuario para el sistema
        except Cliente.DoesNotExist:
            Cliente.objects.create(
            nombre = name, num_documento = document, tipo_documento = type_document,
            celular = phone_mobile, email = email, ciudad = city, telefono = phone, direccion = address
            )
            #generar una contraseña
            client = Cliente.objects.get(num_documento = document)
            def generate_password():
               password = secrets.token_hex(4)
               return password

            #datos que se enviarán al correo 
            password = generate_password()    
            subject = 'Contraseña de Enlasa'
            message_email = f'Buen día señor(a) {name} su contraseña es: {password}.\nLe recomendamos cambiarla.'
            sender = settings.EMAIL_HOST_USER 
            recipient = [email]

            #envío de la contraseña al correo
            send_mail(subject, message_email, sender, recipient)

            #creación de el usuario para el inicio de sesión  
            Usuario.objects.create(num_documento= document, rol = 'CLIENTE',  nombre = name, email= email, password = make_password(password))           
        
                
        #crear póliza
        Poliza.objects.create(fecha_inicio = start_date, fecha_vencimiento = end_date,
         valor = value_premium, prima = type_premium, estado = state, aseguradora_id = insurer, 
         seguro_id = insurance, cliente_id = client, medio_pago = payment_method
        )

        #modal que comunica si el registro fue éxitoso
        modal = True
        message_modal = 'Póliza agregada con éxito.'

    #variables que van al template    
    context = {
        'insurances': Seguro.objects.all(),
        'insurers': Aseguradora.objects.all(),
        'modal': modal,
        'message': message_modal,
    }   

    return render(request, 'admin/add_client.html',{
         'context': context       
    })

def show_clients(request):
    clients = Cliente.objects.all()
    if request.method == 'POST':
        type_document = request.POST.get('typeDocument')
        
        if type_document:
            clients = Cliente.objects.filter(tipo_documento = type_document)
            
    return render(request, 'admin/show_clients.html', {
        'clients': clients
    })

def show_policys(request):
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

    return render(request, 'admin/show_policys.html',{
         'context': context       
    })

def show_claims(request): 
    context = {
        'claims' : Siniestro.objects.all(),
        'insurers': Aseguradora.objects.all(),
        'insurances': Seguro.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
    } 
    if request.method == 'POST':
        insurer = request.POST.get('insurer')
        type_insurance = request.POST.get('type_insurance')
        insurance = request.POST.get('insurance')
        state = request.POST.get('state')
        date = request.POST.get('date')

        filters = {}
        if date:
            filters['fecha'] = date

        if insurer and not "":
            filters['poliza_id__aseguradora_id'] = insurer

        if insurance and not "":
            filters['poliza_id__seguro_id'] = insurance

        if type_insurance and not "":
            filters['poliza_id__seguro_id__tipo_seguro_id'] = type_insurance

        if state and not "":
            filters['estado'] = state
            
        claims = Siniestro.objects.filter(**filters)
        context['claims'] = claims

    return render(request, 'admin/show_claims.html',{
        'context': context       
    })

def add_insurer(request):
    modal = False
    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        Aseguradora.objects.create(nombre = name, telefono = phone, direccion = address)
        modal = True
        message = f'La aseguradora {name} ha sido agregada.'
    
    context = {
        'modal': modal,
        'message': message,
    } 

    return render(request, 'admin/add_insurer.html',{
         'context': context       
    })


def show_insurers(request):
    insurers = Aseguradora.objects.all()
    return render(request, 'admin/show_insurers.html', {
        'insurers': insurers
    })

def add_type_insurance(request):
    modal = False
    message = ''
    if request.method == 'POST':
        name = request.POST.get('type')
        Tipo_Seguro.objects.create(nombre = name)       
        modal = True
        message = f'El tipo de seguro:  {name}, ha sido agregado.'
    
    context = {
    'modal': modal,
    'message': message,
    } 

    return render(request, 'admin/add_type_insurance.html',{
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

def add_insurance(request):
    modal = False
    message = ''
    types_insurances = Tipo_Seguro.objects.all()
    if request.method == 'POST':
        insurance = request.POST.get('type')
        type_insurance_id = int(request.POST.get('typeInsurance'))
        type_insurance = Tipo_Seguro.objects.get(id = type_insurance_id)
        Seguro.objects.create(nombre = insurance, tipo_seguro_id = type_insurance)
        modal = True
        message = f'El seguro: {insurance}, ha sido agregado.'

    context = {
    'modal': modal,
    'message': message,
    'types_insurances': types_insurances,
    } 

    return render(request, 'admin/add_insurance.html',{
         'context': context       
    })

def show_types_insurances(request):
    types_insurances = Tipo_Seguro.objects.all()
    return render(request, 'admin/show_types_insurances.html', {
        'types_insurances': types_insurances
    })   

def show_insurances(request):
    insurances = Seguro.objects.all()
    return render(request, 'admin/show_insurances.html', {
        'insurances': insurances
    })  

def edit_policy(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    modal = False
    message = ''

    if request.method == 'POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('expiryDate')
        premium = request.POST.get('typeFace')
        value_premium = request.POST.get('valueFace')
        payment_method = request.POST.get('payMethod')
        state = request.POST.get('state')

        if start_date:
           policy.fecha_inicio = start_date

        if end_date:
           policy.fecha_vencimiento = end_date

        if value_premium:
           policy.valor = value_premium

        policy.medio_pago = payment_method
        policy.estado = state
        policy.prima = premium
        policy.save()
        modal = True
        message = 'Se agregaron los cambios con éxito.'

    context = {
        'policy': policy,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_policy.html',{
        'context': context       
    })

def edit_client(request, client_id):
    client = Cliente.objects.get(num_documento = client_id) #póliza
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')
        mobile_phone = request.POST.get('phone')
        phone = request.POST.get('phone2')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if name:
           client.nombre = name

        if document:
           client.num_documento = document

        if mobile_phone:
           client.celular = mobile_phone

        if phone:
           client.telefono = phone

        if email:
           client.email = email
        
        if city:
           client.ciudad = city
        
        if address:
           client.direccion = address
        
        client.tipo_documento = type_document
        client.save()
        modal = True
        message = 'Se agregaron los cambios con éxito.'

    context = {
        'client': client,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_client.html',{
        'context': context       
    })

def edit_claim(request, claim_id):
    claim = Siniestro.objects.get(id = claim_id) #siniestro
    modal = False
    message = ''

    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        state = request.POST.get('state')

        if date:
           claim.fecha = date

        if description:
           claim.descripcion = description
       
        claim.estado = state
        claim.save()
        modal = True
        message = 'Se agregaron los cambios con éxito.'

    context = {
        'claim': claim,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_claim.html',{
        'context': context       
    })
    
def edit_type_insurance(request, type_insurance_id):
    type_insurance = Tipo_Seguro.objects.get(id = type_insurance_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        modal = True
    
        if name:
            type_insurance.nombre = name
            message = 'Cambios hechos con éxito.'
        else:           
            message = 'No se pudieron hacer los cambios.' 

    context = {
        'type_insurance': type_insurance,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_types_insurances.html',{
        'context': context       
    })


def edit_insurance(request, insurance_id):
    insurance = Seguro.objects.get(id = insurance_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        modal = True
    
        if name != "":
            insurance.nombre = name
            insurance.save()
            message = 'Cambios hechos con éxito.'
        
        else:
           message = 'No se pudieron hacer los cambios.' 

    context = {
        'insurance': insurance,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_insurance.html',{
        'context': context       
    })

def delete_claim(request, claim_id):
    claim = Siniestro.objects.get(id = claim_id)
    claim.delete()
    return redirect('show_claims')

def delete_client(request, client_id):
    client = Cliente.objects.get(num_documento = client_id)

    policys = Poliza.objects.filter(cliente_id = client)

    if policys.exists():
        messages.error(request, 'No se puede eliminar el cliente porque tiene pólizas asociadas.')
        return redirect('show_clients')
    
    else:
        client.delete()
        messages.success(request, 'Cliente eliminado con éxito.')
        return redirect('show_clients')

def delete_policy(request, policy_id):
    policy = Poliza.objects.get(id = policy_id)

    if policy.fecha_vencimiento <= date.today():
        policy.delete()
        messages.success(request, 'Póliza eliminada con éxito.')

    else:
        messages.error(request, 'No se pudo eliminar la póliza porque no ha vencido.')

    return redirect('show_policys')

def edit_profile_admin(request, admin_id):
    admin = Usuario.objects.get(num_documento = admin_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        modal = True
    
        if name:
            admin.nombre = name

        if email:
            admin.email = email

        admin.save()
        message = 'Cambios guardados con éxito.' 

    context = {
        'admin': admin,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_profile.html',{
        'context': context       
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


def beneficiarys_client(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    beneficiarys = policy.policy_beneficiary_set.all() 

    if request.method == 'POST':
        type_document = request.POST.get('typeDocument')
        
        if type_document:
            beneficiarys = policy.policy_beneficiary_set.filter(beneficiary_id__tipo_documento = type_document)

    context = {
    'beneficiarys' : beneficiarys,
    } 

    return render(request, 'cliente/misBeneficiarios.html',{
         'context': context       
    })

def claims_client(request, policy_id):
    policy = Poliza.objects.get(id = policy_id)
    claims = Siniestro.objects.filter(poliza_id = policy)
 
    if request.method == 'POST':
        state = request.POST.get('state')
        date = request.POST.get('date')

        filters = {}
        if date:
            filters['fecha'] = date

        if state and not "":
            filters['estado'] = state
            
        new= claims.filter(**filters)
        claims = new

    return render(request, 'cliente/claims.html',{
        'claims': claims      
    })


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
 
    context = {
    'modal': modal,
    'message': message,
    'insurer': insurer
    } 

    return render(request, 'admin/edit_insurer.html',{
         'context': context       
    }) 

#vista que agrega  beneficiarios a la póliza seleccionada
def add_beneficiary(request, policy_id):   
    policy = Poliza.objects.get(id = policy_id)
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener datos del form
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')

        try:
            #crear beneficiario
            beneficiary = Beneficiario.objects.create(num_documento= document, nombre = name, tipo_documento = type_document)
            Policy_Beneficiary.objects.create(policy_id = policy, beneficiary_id = beneficiary) #crear relación con la póliza
            modal = True
            message = f'La persona {name} fue agregado como beneficario a la póliza {policy.seguro_id.nombre} a cargo del señor(a) {policy.cliente_id.nombre}'

        except Exception as e:
            message = f'Error al crear beneficiario: {e}'
    
                   
    context = {
    'modal': modal,
    'message': message,
    'policy' :policy,
    } 

    return render(request, 'admin/addBeneficiary.html',{
         'context': context       
    })

#vista que muestra los beneficiarios de la poliza seleccionada
def show_beneficiarys(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    beneficiarys = policy.policy_beneficiary_set.all() 

    if request.method == 'POST':
        type_document = request.POST.get('typeDocument')
        
        if type_document:
            beneficiarys = policy.policy_beneficiary_set.filter(beneficiary_id__tipo_documento = type_document)

    context = {
    'beneficiarys' : beneficiarys,
    } 

    return render(request, 'admin/showBeneficiarys.html',{
         'context': context       
    })

#vista para agregar un siniestro a la póliza seleccionada
def add_claim(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    modal = False
    message = ''

    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        state = request.POST.get('state')
        
        #crear siniestro
        try:
            Siniestro.objects.create(fecha = date, descripcion = description, estado = state, poliza_id = policy)
            modal = True
            message = f'El siniestro fue creado a la póliza {policy.seguro_id.nombre} a cargo del señor(a) {policy.cliente_id.nombre}'

        except Exception as e:
            modal = True
            message = f'Error al crear el siniestro: {e}'

    context = {
    'modal': modal,
    'message': message,
    } 

    return render(request, 'admin/add_claim.html',{
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