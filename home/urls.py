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
    path('admin_dashboard/', views.admin_dashboard, name= 'admin_principal'),
    path('admin_dashboard/profile/', views.admin_profile, name= 'admin_profile'),
    path('admin_dashboard/clients/', views.show_clients, name='show_clients'),
    path('admin_dashboard/add_client/', views.create_client_policy, name='add_client'),
    path('admin_dashboard/claims/', views.show_claims, name='show_claims'),
    path('admin_dashboard/insurers', views.show_insurers, name='show_insurers'),
    path('admin_dashboard/add_insurer/', views.add_insurer, name='add_insurer'),
    path('admin_dashboard/types_insurances/', views.show_types_insurances, name='show_types_insurances'),
    path('admin_dashboard/add_type_insurance', views.add_type_insurance, name='add_type_insurance'),
    path('admin_dashboard/insurances/', views.show_insurances, name='show_insurances'),
    path('dmin_dashboard/add_insurance', views.add_insurance, name='add_insurance'),
    path('admin_dashboard/policys/', views.show_policys, name = 'show_policys'),
    path('admin_dashboard/aseguradoras/<int:insurer_id>/', views.edit_insurer, name='edit'),
    path('admin_dashboard/add_beneficiary/<int:policy_id>/', views.add_beneficiary, name='add_beneficiary'),
    path('admin_dashboard/show_beneficiarys/<int:policy_id>/', views.show_beneficiarys, name='show_beneficiarys'),
    path('admin_dashboard/add_claim/<int:policy_id>/', views.add_claim, name='add_claim'),
    path('admin_dashboard/edit_policy/<int:policy_id>/', views.edit_policy, name='edit_policy'),
    path('admin_dashboard/edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('admin_dashboard/edit_claim/<int:claim_id>/', views.edit_claim, name='edit_claim'),
]
#URLs del apartado cliente*
cliente_urls = [
    path('cliente/', views.principalCliente, name='cliente_principal'),
    path('cliente/mi-perfil/', views.miPerfil, name='cliente_mi_perfil'),
    path('cliente/polizas/', views.misPolizas, name='cliente_mis_polizas'),
    path('cliente/polizas/beneficiarys/<int:policy_id>/', views.beneficiarys_client, name='client_beneficiarys'),
    path('show_my_claims/<int:policy_id>/', views.claims_client, name='show_my_claims'),
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