from .models import Tipo_Seguro, Seguro, Usuario, Aseguradora, Usuario, Cliente, Poliza, Beneficiario, Policy_Beneficiary, Siniestro
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
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

#vista que inicia sesión en el sistema
def login_user(request):
    modal = False
    message = ''
    if request.method == 'POST':
        
        #obtener los datos del formulario
        documento = request.POST.get('numDocument')
        contraseña = request.POST.get('password')

        usuario = authenticate(num_documento = documento, password = contraseña) #verificar si el usuario es válido
        if usuario is not None:
            login(request, usuario) #iniciar la sesión

            #condicional para redirigirlo a su respectivo panel según su rol
            if usuario.rol == settings.ROLE_CLIENTE:
               redirect_url = settings.ROLE_REDIRECT_URLS.get(usuario.rol) 
               return redirect(redirect_url)

            elif usuario.rol == settings.ROLE_ADMINISTRADOR:
                redirect_url = settings.ROLE_REDIRECT_URLS.get(usuario.rol)
                return redirect(redirect_url)

            else:
                #redirección al rol de gerente
                redirect_url = settings.ROLE_REDIRECT_URLS.get('GERENTE')
                return redirect(redirect_url )
        else:
            modal = True
            message = 'Datos no válidos'
    
    context = {
        'modal': modal,
        'message': message,
    }

    return render(request, 'public/login.html',{
        'context': context       
    })


#vista para ver la principal de administrador
@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

#vista para ver el perfil del administrador
@login_required
def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

#vista para crear un cliente si no existe y su respectiva póliza
@login_required
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

#vista para ver el listado de clientes
@login_required
def show_clients(request):
    clients = Cliente.objects.all()

    if request.method == 'POST': #obtener datos del formulario cuando se vaya a filtrar
        type_document = request.POST.get('typeDocument')
        
        if type_document:
            clients = Cliente.objects.filter(tipo_documento = type_document) #clientes filtrados
            
    return render(request, 'admin/show_clients.html', {
        'clients': clients
    })

#vista para ver el listado de pólizas
@login_required
def show_policys(request):
    policys = Poliza.objects.all()

    #datos que van para el template
    context = {
        'insurances': Seguro.objects.all(),
        'insurers': Aseguradora.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
        'policys': policys,
    }  
    if request.method == 'POST':
        #obtener datos del formulario de filtrar
        date_star = request.POST.get('startDate')
        date_end = request.POST.get('expiryDate')
        insurer = request.POST.get('insurer')
        insurance = request.POST.get('insurance')
        type_insurance = request.POST.get('type_insurance')
        state = request.POST.get('state')

        filters = {} #diccionario para almacenar los filtros
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
  
        policys = Poliza.objects.filter(**filters) #filtrar pólizas por los datos almacenados en el diccionario
        context['policys'] = policys

    return render(request, 'admin/show_policys.html',{
         'context': context       
    })

#vista para ver los siniestros
@login_required
def show_claims(request):

    #datos que van al template 
    context = {
        'claims' : Siniestro.objects.all(),
        'insurers': Aseguradora.objects.all(),
        'insurances': Seguro.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
    } 
    if request.method == 'POST':
        #obtener datos del formulario filtrar
        insurer = request.POST.get('insurer')
        type_insurance = request.POST.get('type_insurance')
        insurance = request.POST.get('insurance')
        state = request.POST.get('state')
        date = request.POST.get('date')

        filters = {} #diccionario que almacena los filtros
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
            
        claims = Siniestro.objects.filter(**filters) #filtrar siniestros por los datos almacenados en el diccionario de filtros
        context['claims'] = claims

    return render(request, 'admin/show_claims.html',{
        'context': context       
    })

#vista para agregar una aseguradora
@login_required
def add_insurer(request):
    modal = False
    message = ''
    add = False 
    if request.method == 'POST':
        #obtener datos del formulario
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        modal = True
        
        #validar datos del formulario
        if name and phone and address:
           Aseguradora.objects.create(nombre = name, telefono = phone, direccion = address) #crear aseguradora
           add = True      
           message = f'La aseguradora {name} ha sido agregada.'

        else:
            add = False
            message = 'Complete los campos'
    
    context = { #datos que van al template
        'add' : add,
        'modal': modal,
        'message': message,
    } 

    return render(request, 'admin/add_insurer.html',{
         'context': context       
    })

#vista para ver la lista de aseguradoras
@login_required
def show_insurers(request):
    insurers = Aseguradora.objects.all()
    return render(request, 'admin/show_insurers.html', {
        'insurers': insurers
    })

#vista para ver los tipos de seguros
@login_required
def add_type_insurance(request):
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener los datos del formulario
        name = request.POST.get('type')
        modal = True

        if name:
           Tipo_Seguro.objects.create(nombre = name)            
           message = f'El tipo de seguro:  {name}, ha sido agregado.'

        else:
            message = 'Complete los campos'
    
    context = {
    'modal': modal,
    'message': message,
    } 

    return render(request, 'admin/add_type_insurance.html',{
         'context': context       
    })

#vista que agrega un seguro a la lista
@login_required
def add_insurance(request):
    modal = False
    message = ''
    types_insurances = Tipo_Seguro.objects.all() #obtener los tipos de seguros para poder agregar el seguro a alguno

    if request.method == 'POST':
        #obtenener los datos del formualrio
        insurance = request.POST.get('type')
        type_insurance_id = int(request.POST.get('typeInsurance'))
        modal = True

        if insurance:
           type_insurance = Tipo_Seguro.objects.get(id = type_insurance_id)  #obtener el tipo de seguro al que va a pertenecer
           Seguro.objects.create(nombre = insurance, tipo_seguro_id = type_insurance) #crear el seguro
           message = f'El seguro: {insurance}, ha sido agregado.'

        else:
            message = 'No se completaron los campos.'

    context = { #datos que van al template
    'modal': modal,
    'message': message,
    'types_insurances': types_insurances,
    } 

    return render(request, 'admin/add_insurance.html',{
         'context': context       
    })

#vista que muestra los tipos de seguros en portafolio
@login_required
def show_types_insurances(request):
    types_insurances = Tipo_Seguro.objects.all()
    return render(request, 'admin/show_types_insurances.html', {
        'types_insurances': types_insurances
    })   

#vista que muestra los seguros en portafolio
@login_required
def show_insurances(request):
    insurances = Seguro.objects.all()
    return render(request, 'admin/show_insurances.html', {
        'insurances': insurances
    })  

#vista que edita una póliza: obtiene la póliza por la url
@login_required
def edit_policy(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener datos del formulario
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('expiryDate')
        premium = request.POST.get('typeFace')
        value_premium = request.POST.get('valueFace')
        payment_method = request.POST.get('payMethod')
        state = request.POST.get('state')

        #validar datos del formulario que no son select
        if start_date:
           policy.fecha_inicio = start_date

        if end_date:
           policy.fecha_vencimiento = end_date

        if value_premium:
           policy.valor = value_premium

        #guardar datos 
        policy.medio_pago = payment_method
        policy.estado = state
        policy.prima = premium
        policy.save()

        #mosatrar mensaje
        modal = True
        message = 'Se agregaron los cambios con éxito.'

    context = { #datos que van al template
        'policy': policy,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_policy.html',{
        'context': context       
    })

#vista que edita datos del cliente: obtiene el cliente por la url
@login_required
def edit_client(request, client_id):
    client = Cliente.objects.get(num_documento = client_id) #cliente
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener datos del formulario
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')
        mobile_phone = request.POST.get('phone')
        phone = request.POST.get('phone2')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')
        
        #validar los datos del formulario
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
        client.save() #guardar cambios
        modal = True
        message = 'Se agregaron los cambios con éxito.'
   
    context = { #datos que van al template
        'client': client,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_client.html',{
        'context': context       
    })

#vista que cambia la contraseña del cliente: obtiene el usuario del cliente por url
@login_required
def change_password_client(request, client_id):
    manager = Usuario.objects.get(num_documento = client_id)
    modal = False
    changed = False
    message = ''

    if request.method == 'POST':
        #obtener datos del formulario
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        modal = True
        
        if old_password and new_password: #validar datos
            
            #validar si la contraseña antigua dada es igual a la existente
            if check_password(old_password, manager.password):
                manager.password = make_password(new_password) #cambiar contraseña por la nueva
                manager.save()
                changed = True
                message = 'Cambio de contraseña éxitoso, vuelve a ingresar.' 
                logout(request) #terminar sesión para que vuelva e ingrese

            else:
                #mostrar mensaje en caso de no coincidir datos
                changed = False
                message = 'La contraseña antigua no coincide.' 
        else:
            #mostrar mensaje en caso de no llenar los campos del formulario
            changed = False
            message = 'Porfavor complete los campos.' 
 

    context = { #datos que se enviarán al template
        'changed': changed,
        'modal' : modal,
        'message': message
    }

    return render(request, 'cliente/change_password_client.html',{
        'context': context       
    })

#vista que edita un siniestro: obtiene el siniestro por la url
@login_required
def edit_claim(request, claim_id):
    claim = Siniestro.objects.get(id = claim_id) #siniestro
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener datos del formulario
        date = request.POST.get('date')
        description = request.POST.get('description')
        state = request.POST.get('state')
        
        #validar datos
        if date:
           claim.fecha = date

        if description:
           claim.descripcion = description
        
        #guardar datos
        claim.estado = state
        claim.save()

        #mostrar mensaje
        modal = True
        message = 'Se agregaron los cambios con éxito.'
    
    context = { #pasar datos al template
        'claim': claim,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_claim.html',{
        'context': context       
    })

#vista que edita el nombre de un tipo de seguro: obtiene el id del tipo de seguro por la url
@login_required  
def edit_type_insurance(request, type_insurance_id):
    type_insurance = Tipo_Seguro.objects.get(id = type_insurance_id)
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        modal = True
    
        if name:
            type_insurance.nombre = name #cambiar el nombre existente por el dado
            message = 'Cambios hechos con éxito.'
            type_insurance.save() #guardar cambios
        else:           
            message = 'No se pudieron hacer los cambios.' 

    #diccionario que almacena los datos que van al template
    context = {
        'type_insurance': type_insurance,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_types_insurances.html',{
        'context': context       
    })


#vista que edita el nombre de un seguro: obtiene el id del seguro el url
@login_required
def edit_insurance(request, insurance_id):
    insurance = Seguro.objects.get(id = insurance_id) 

    #modal para mostrar el mensaje
    modal = False
    message = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        modal = True
    
        if name:
            insurance.nombre = name #cambiar el nombre existente por el nombre dado
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

#vista que elimina un siniestro: obtiene el id del siniestro por la url
@login_required
def delete_claim(request, claim_id):
    claim = Siniestro.objects.get(id = claim_id)
    claim.delete()
    return redirect('show_claims') #rredirigir a la vista de siniestros


#vista que elimina un cliente: obtiene el id del cliente por la url
@login_required
def delete_client(request, client_id):
    client = Cliente.objects.get(num_documento = client_id)

    policys = Poliza.objects.filter(cliente_id = client)#filtra las pólizas del cliente
    
    #condicional: si tiene pólizas relacionadas no se elimina el cliente
    if policys.exists():
        messages.error(request, 'No se puede eliminar el cliente porque tiene pólizas asociadas.')
        return redirect('show_clients')
    
    #si no tiene pólizas relacionadas se elimina
    else:
        client.delete()
        messages.success(request, 'Cliente eliminado con éxito.')
        return redirect('show_clients')

#vista que elimina una póliza: obtiene la póliza por la url
@login_required
def delete_policy(request, policy_id):
    policy = Poliza.objects.get(id = policy_id)
    
    #condicional: si la póliza ya venció se elimina
    if policy.fecha_vencimiento <= date.today():
        policy.delete()
        messages.success(request, 'Póliza eliminada con éxito.')

    #si no ha vencido no se puede eliminar
    else:
        messages.error(request, 'No se pudo eliminar la póliza porque no ha vencido.')
    
    #redirigir a la vista de pólizas
    return redirect('show_policys')

#vista que edita la vista: obtiene al administrador por la url
@login_required
def edit_profile_admin(request, admin_id):
    admin = Usuario.objects.get(num_documento = admin_id)
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener datos del formulario
        name = request.POST.get('name')
        email = request.POST.get('email')
        modal = True
        
        #validar datos que no sean vacíos
        if name:
            admin.nombre = name 

        if email:
            admin.email = email
        
        admin.save() #guardar la información editada
        message = 'Cambios guardados con éxito.' 
    
    context = { #pasar datos al template
        'admin': admin,
        'modal' : modal,
        'message': message
    }

    return render(request, 'admin/edit_profile.html',{
        'context': context       
    })

#vista que edita las aseguradoras: se obtiene la aseguradora por la url
@login_required
def edit_insurer(request, insurer_id):
    insurer = Aseguradora.objects.get(id = insurer_id)
    modal = False
    message = ''

    if request.method == 'POST':
        #se obtienen los datos del formulario
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        #validar datos
        if name:
           insurer.nombre = name
        
        if phone:
           insurer.telefono = phone

        if address:           
           insurer.direccion = address

        insurer.save() #guardar cambios
        modal = True
        message = 'Se realizaron los cambios exitosamente.'
 
    context = { #datos que van para el template
    'modal': modal,
    'message': message,
    'insurer': insurer
    } 

    return render(request, 'admin/edit_insurer.html',{
         'context': context       
    }) 

#vista que agrega  beneficiarios a la póliza seleccionada
@login_required
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
@login_required
def show_beneficiarys(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    beneficiarys = policy.policy_beneficiary_set.all() #se obtiene los beneficiarios de la póliza

    if request.method == 'POST':
        #obtener datos del formulario en caso de filtrar
        type_document = request.POST.get('typeDocument')
        
        #validar datos
        if type_document:
            #filtrar pólizas por el dato recibido
            beneficiarys = policy.policy_beneficiary_set.filter(beneficiary_id__tipo_documento = type_document)

    context = { #datos que van al template
    'beneficiarys' : beneficiarys,
    } 

    return render(request, 'admin/showBeneficiarys.html',{
         'context': context       
    })

#vista para agregar un siniestro a la póliza seleccionada
@login_required
def add_claim(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener los datos del formulario
        date = request.POST.get('date')
        description = request.POST.get('description')
        state = request.POST.get('state')
        
        if date and description and state:
            #crear siniestro
            try:
                Siniestro.objects.create(fecha = date, descripcion = description, estado = state, poliza_id = policy)
                modal = True
                message = f'El siniestro fue creado a la póliza {policy.seguro_id.nombre} a cargo del señor(a) {policy.cliente_id.nombre}'

            except Exception as e:
                modal = True
                message = f'Error al crear el siniestro: {e}'
        else:
            message = 'Complete los campos.'

    context = { #datos que van al template
    'modal': modal,
    'message': message,
    } 

    return render(request, 'admin/add_claim.html',{
         'context': context       
    })

#vistas del apartado cliente

#vista para ver el apartado principal del cliente
@login_required
def principalCliente(request):
    return render(request, 'cliente/principal.html')

#vista para ver el perfil del cliete
@login_required
def miPerfil(request):
    documento = request.user.num_documento
    cliente = Cliente.objects.get(num_documento = documento)
    
    return render(request, 'cliente/miPerfil.html', {
        'cliente': cliente
    })
    return render(request, 'cliente/miPerfil.html')

#vista para ver las pólizas de cada cleinte
@login_required
def misPolizas(request):
    documento = request.user.num_documento
    cliente = Cliente.objects.get(num_documento = documento)
    policys_all = Poliza.objects.filter(cliente_id = cliente) #filtrar las pólizas del cliente

    context = { #datos que van al template
        'insurers': Aseguradora.objects.all(),
        'insurances': Seguro.objects.all(),
        'type_insurance': Tipo_Seguro.objects.all(),
        'policys': policys_all,
    } 
    if request.method == 'POST':
        #obtener los datos del formulario en caso de filtrar
        date_star = request.POST.get('startDate')
        date_end = request.POST.get('expiryDate')
        insurer = request.POST.get('insurer')
        insurance = request.POST.get('insurance')
        type_insurance = request.POST.get('type_insurance')
        state = request.POST.get('state')

        filters = {} #diccionario para almacenar los items para filtrar
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
            
        policys = policys_all.filter(**filters) #filtrar las pólizas por los datos almacenados en la variable filters
        context['policys'] = policys

    return render(request, 'cliente/misPolizas.html',{
        'context': context       
    })

#vista para ver los beneficiarios de cada póliza del cliente: obtenido la póliza por la url
@login_required
def beneficiarys_client(request, policy_id):
    policy = Poliza.objects.get(id = policy_id) #póliza
    beneficiarys = policy.policy_beneficiary_set.all() #obtener beneficiarios

    if request.method == 'POST':
        #obtener datos en caso de filtrar
        type_document = request.POST.get('typeDocument')
        
        #validar datos
        if type_document:
            #obtener a los beneficiarios filtrados
            beneficiarys = policy.policy_beneficiary_set.filter(beneficiary_id__tipo_documento = type_document)

    context = {
    'beneficiarys' : beneficiarys,
    } 

    return render(request, 'cliente/misBeneficiarios.html',{
         'context': context       
    })

#vista que muestra los siniestros de la póliza de un cliente: se obtiene la póliza por la url
@login_required
def claims_client(request, policy_id):
    policy = Poliza.objects.get(id = policy_id)
    claims = Siniestro.objects.filter(poliza_id = policy) #filtrar siniestros de la póliza
 
    if request.method == 'POST':
        #obtener datos del formulario en caso de filtrar
        state = request.POST.get('state')
        date = request.POST.get('date')

        filters = {} #alamcenar filtros
        #validar datos
        if date:
            filters['fecha'] = date

        if state and not "":
            filters['estado'] = state
            
        new= claims.filter(**filters) #obtener los siniestros filtrados
        claims = new

    return render(request, 'cliente/claims.html',{
        'claims': claims      
    })

#vista que edita el perfil de un cliente: se obtiene el cliente mediante la url
@login_required
def edit_profile_client(request, client_id):

    #se obtiene tanto al usuario como al cliente
    user = Usuario.objects.get(num_documento = client_id)
    client = Cliente.objects.get(num_documento = client_id)

    modal = False
    message = ''

    if request.method == 'POST':
        #se obtienen los datos dados en el formulario
        name = request.POST.get('name')
        type_document = request.POST.get('typeDocument')
        document = request.POST.get('document')
        phone_mobile = request.POST.get('phone')
        phone = request.POST.get('phone2')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')

        modal = True    
        
        #se validan los datos: editar si es diferente al dato almacenado
        #se edita también los campos compartidos en usuario
        if name and client.nombre != name: 
            client.nombre = name
            user.nombre = name

        if client.tipo_documento != type_document:
           client.tipo_documento = type_document

        if document and client.num_documento != document:
            client.num_documento = document
            user.num_documento = document #dato compartido con usuario

        if phone_mobile and client.celular != phone_mobile:
            client.celular = phone_mobile

        if phone and client.telefono != phone:
            client.telefono = phone

        if email and client.email != email:
            client.email = email
            user.email = email  #dato compartido con usuario
        
        if city and client.ciudad != city:
            client.ciudad = ciudad

        if address and client.direccion != address:
            client.direccion = address
        
        #guardar cambios hechos tanto para cliente como para el usuario del sistema del cliente
        client.save()
        user.save()
        message = 'Cambios guardados con éxito.' 
    
    context = { #datos que van para el template
        'client': client,
        'modal' : modal,
        'message': message
    }

    return render(request, 'cliente/edit_profile_client.html',{
        'context': context       
    })



#vistas del apartado gerente
#página princal del gerente
@login_required
def principalGerente(request):
    return render(request, 'gerente/principal.html')

#vista para ver el perfil del gerente
@login_required
def verPerfilGerente(request):
    return render(request, 'gerente/verPerfil.html')

#vista para editar el perfil del gerente: se obtiene al gerente mediante la url
@login_required
def edit_profile_manager(request, manager_id):
    manager = Usuario.objects.get(num_documento = manager_id)
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener los datod del formulario
        name = request.POST.get('name')
        email = request.POST.get('email')

        modal = True
        
        #validar datos
        if name:
            manager.nombre = name

        if email:
            manager.email = email

        manager.save() #guardar cambios
        message = 'Cambios guardados con éxito.' 
   
    #datos que se van a utilizar en le template
    context = {
        'manager': manager,
        'modal' : modal,
        'message': message
    }

    return render(request, 'gerente/edit_profile_manager.html',{
        'context': context       
    })

#vista que cambia la contraseña del gerente: se obtiene al gerente mediante la url
@login_required
def change_password_manager(request, manager_id):
    manager = Usuario.objects.get(num_documento = manager_id)
    modal = False
    changed = False
    message = ''

    if request.method == 'POST':
        #se obtienen los datos del formulario
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')

        modal = True
        
        #validar datos del formualario
        if old_password and new_password:
            
            #verifica si la contraseña antigua es igual a la dada
            if check_password(old_password, manager.password):
                manager.password = make_password(new_password) #crear la nueva contraseña cifrada
                manager.save()
                changed = True
                message = 'Cambio de contraseña éxitoso, vuelve a ingresar.' 
                logout(request) #cerrar sesión

            #caso en el que la contraseña dada no coincida
            else:
                changed = False
                message = 'La contraseña antigua no coincide.'
        #caso para cuando no se completan los campos 
        else:
            changed = False
            message = 'Porfavor complete los campos.' 
   
    context = { #datos que van al template
        'changed': changed,
        'modal' : modal,
        'message': message
    }

    return render(request, 'gerente/change_password_manager.html',{
        'context': context       
    })

#vista que edita la contraseña de un administrador: se obtiene al administrador mediante la url
@login_required
def edit_password_admin(request, admin_id):
    admin = Usuario.objects.get(num_documento = admin_id)
    modal = False
    message = ''

    if request.method == 'POST':
        #obtener los datos del formulario
        new_password = request.POST.get('newPassword')
        modal = True
        
        #validar datos
        if new_password:
            admin.password = make_password(new_password) #crear contraseña con el cifradi
            admin.save()
            message = 'Cambio de contraseña éxitoso.' 

        else:
            changed = False
            message = 'Porfavor complete los campos.' 
   
    context = { #datos que van para el template
        'modal' : modal,
        'message': message
    }

    return render(request, 'gerente/edit_password_admin.html',{
        'context': context       
    })

#vista que elimina un administrador: se obtiene al administrador mediante la url
@login_required
def delete_admin(request, admin_id):
    admin = Usuario.objects.get(num_documento = admin_id)
    admin.delete()
    messages.success(request, 'Administrador eliminado con éxito.')
    return redirect('gerente_administradores_list')

#vista que agrega un administrador
@login_required
def agregarAdministrador(request):
    modal = False
    mensaje = ''

    if request.method == 'POST':
        #obtener datos del formulario
        name = request.POST.get('name')  
        email = request.POST.get('email')
        password = request.POST.get('password')
        modal = True

        #funcion para crear un usuario
        def generar_usuario():
            return random.sample(range(10), 8)   

        numero = generar_usuario()
        usuario = int("".join(map(str, numero))) #converirlo en número porque viene en lista

        #validar datos 
        if name and email and password:           
            Usuario.objects.create(num_documento= usuario, rol = 'ADMINISTRADOR',  nombre = name, email= email, password = make_password(password))              
            mensaje = f'Se ha agregado a {name} como administrador.'
            #datos que se enviarán al correo    
            subject = 'Contraseña de Enlasa'
            message_email = f'Buen día señor(a) {name}, haz sido agregad@ como administrador de Enlasa, tus datos para el inicio de sesión son:\nContraseña: {password}\nUsuario: {usuario}\n¡Bienvenido administrador!.'
            sender = settings.EMAIL_HOST_USER 
            recipient = [email]

            #envío de la contraseña al correo
            send_mail(subject, message_email, sender, recipient)

        else:
            mensaje = 'No se pudo agregar, por favor complete los campos.'

    
    context = { #datos que van para el template
    'modal': modal,
    'mensaje': mensaje,
    } 

    return render(request, 'gerente/agregarAdministrador.html',{
         'context': context       
    })

#vista qie muestra los administradores
@login_required
def verAdministradores(request):
    usuarios = Usuario.objects.all()
    administradores = []
    for usuario in usuarios:
        if usuario.rol == 'ADMINISTRADOR':
            administradores.append(usuario) #almacenar los usuarios que tengan el rol de administrador
         
    return render(request, 'gerente/verAdministradores.html', {
        'administradores': administradores
    })  

#vista para ver estadísticas generales
@login_required
def verEstadisticasGenerales(request):
    policys_activate = Poliza.objects.filter(estado = True)
    policys_not_activate = Poliza.objects.filter(estado = False)
    types_insurances = Tipo_Seguro.objects.all()
    names = [] #almacena los nombres de los tipos de seguros(4)
    data = [] #almacena los datos de cada tipo de seguros (4)

    data_others = 0 #almacena los datos del resto de seguros
    count = 0
    for type_insurance in types_insurances:
        #se agregan por separado los datos de los primeros 4
        if count <= 3:
           names.append(type_insurance.nombre)
           data.append(Poliza.objects.filter(seguro_id__tipo_seguro_id = type_insurance).count())

        #el resto se muestra en un solo apartado
        else:
            data_others += Poliza.objects.filter(seguro_id__tipo_seguro_id = type_insurance).count()

        count += 1

    by_state = [policys_activate.count(), policys_not_activate.count()] #almacena las pólizas por estado

    context = { #datos que van para el template
    'by_state': by_state,
    'names_types_insurances': names,
    'data': data,
    'data_others': data_others
    } 

    return render(request, 'gerente/verEstadisticasGenerales.html', context)

#vista para ver estadísticas por aseguradora
@login_required
def verEstadisticasPorAseguradora(request):
    insurers = Aseguradora.objects.all()
    names = [] #almacena los nombres(6)
    data = [] #almacena los datos(6)

    data_others = 0 #alamcena el dato de las otras en uno solo
    count = 0
    for insurer in insurers:
        if count <= 5: #almacena los datos de las primeras 6
           names.append(insurer.nombre)
           data.append(Poliza.objects.filter(aseguradora_id = insurer).count())
        
        else: #el resto lo suma en una sola
            data_others += Poliza.objects.filter(aseguradora_id = insurer).count()

        count += 1

    context = { #datos que van para el template
    'names_insurers': names,
    'data': data,
    'data_others': data_others
    } 

    return render(request, 'gerente/verEstadisticasPorAseguradora.html', context)


#Páginas públicas

def nosotros(request):
    return render(request, 'public/about.html')

def segurosGenerales(request):
    return render(request, 'public/segurosGenerales.html')

def segurosHogar(request):
    return render(request, 'public/segurosHogar.html')

def home(request):
    return render(request,'public/home.html')
def segurosGenerales(request):
    return render(request,'public/segurosGenerales.html')
def segurosHogar(request):
    return render(request,'public/segurosHogar.html')
def segurosObligatorios(request):
    return render(request,'public/segurosObligatorios.html')
def segurosVida(request):
    return render(request,'public/segurosVida.html')
def contactanos(request):
    return render(request,'public/contactanos.html')
def nosotros(request):
    return render(request,'public/nosotros.html')