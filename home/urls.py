from django.urls import path
from . import views

#URLs generales*
general_urls = [
    path('', views.home, name='home'),
    path('login', views.iniciar_sesion, name='login'),
    path('public/nosotros/', views.nosotros, name='nosotros'),
    path('public/segurosGenerales/', views.segurosGenerales, name='segurosGenerales'),
    path('public/segurosHogar/', views.segurosHogar, name='segurosHogar'),
    path('logout/', views.exit, name='exit'),
]
#URLs del apartado administrador
admin_urls = [
    path('administrador/', views.principalAdmin, name= 'admin_principal'),
    path('administrador/perfil/', views.verPerfil, name= 'admin_perfil'),
    path('administrador/clientes/', views.verClientes, name='admin_clientes_list'),
    path('administrador/agregar-cliente/', views.agregarCliente, name='admin_cliente_agregar'),
    path('administrador/siniestros/', views.verSiniestros, name='admin_siniestros_list'),
    path('administrador/agregar-siniestro/', views.agregarSiniestro, name='admin_siniestros_agregar'),
    path('administrador/aseguradoras/', views.verAseguradoras, name='admin_aseguradoras_list'),
    path('administrador/agregar-aseguradora/', views.agregarAseguradora, name='admin_aseguradoras_agregar'),
    path('administrador/tipos-seguros/', views.verTiposSeguros, name='admin_tipos_seguros_list'),
    path('administrador/agregar-tipo-seguro/', views.agregarTipoSeguro, name='admin_tipos_seguros_agregar'),
    path('administrador/seguros/', views.verSeguros, name='admin_seguros_list'),
    path('administrador/agregar-seguro/', views.agregarSeguro, name='admin_seguros_agregar'),
    path('administrador/polizas/', views.verPolizas, name = 'admin_polizas_list'),

    #editar
    path('aseguradoras/<int:insurer_id>/', views.edit_insurer, name='edit'),
    path('add_beneficiary/<int:policy_id>/', views.add_beneficiary, name='add_beneficiary'),
]
#URLs del apartado cliente*
cliente_urls = [
    path('cliente/', views.principalCliente, name='cliente_principal'),
    path('cliente/mi-perfil/', views.miPerfil, name='cliente_mi_perfil'),
    path('cliente/polizas/', views.misPolizas, name='cliente_mis_polizas'),
    path('cliente/polizas/mis-beneficiarios/', views.misBeneficiarios, name='cliente_mis_beneficiarios'),
]
#URLs del apartado gerente
gerente_urls = [
    path('gerente/', views.principalGerente, name='gerente_principal'),
    path('gerente/perfil/', views.verPerfilGerente, name='gerente_perfil'),
    path('gerente/estadisticas-generales/', views.verEstadisticasGenerales, name='gerente_estadisticas_generales'),
    path('gerente/estadisticas-por-aseguradora/', views.verEstadisticasPorAseguradora, name='gerente_estadisticas_aseguradora'),
    path('gerente/administradores/', views.verAdministradores, name='gerente_administradores_list'),
    path('gerente/agregar-admi/', views.agregarAdministrador, name='gerente_administradores_agregar'),
]


urlpatterns = general_urls + admin_urls + cliente_urls + gerente_urls