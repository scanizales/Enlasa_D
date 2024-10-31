from django.urls import path
from . import views

urlpatterns = [  
    path('', views.home, name='home'),
    path('adminPrincipal', views.principalAdmin, name = 'principalAdmin'),
    path('profile', views.verPerfil, name = 'verPerfil'),
    path('agregarCliente', views.agregarCliente, name = 'agregarCliente'),
    path('agregarSiniestro', views.agregarSiniestro, name = 'agregarSiniestro'),
    path('verClientes', views.verClientes, name='verClientes'),
    path('verPolizas', views.verPolizas, name='verPolizas'),
    path('verSiniestros', views.verSiniestros, name='verSiniestros'),
    path('agregarAseguradora', views.agregarAseguradora, name='agregarAseguradora'),
    path('verAseguradoras', views.verAseguradoras, name='verAseguradoras'),
    path('agregarTipoSeguro', views.agregarTipoSeguro, name='agregarTipoSeguro'),
    path('agregarSeguro', views.agregarSeguro, name='agregarSeguro'),
    path('verTiposSeguros', views.verTiposSeguros, name='verTiposSeguros'),
    path('verSeguros', views.verSeguros, name='verSeguros'),

]