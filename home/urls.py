from django.urls import path
from . import views

urlpatterns = [  
    path('', views.home, name='home'),
    path('adminPrincipal', views.principalAdmin, name = 'principalAdmin'),
    path('profile', views.verPerfil, name = 'verPerfil'),
    path('agregarCliente', views.agregarCliente, name = 'agregarCliente'),
    path('agregarSiniestro', views.agregarSiniestro, name = 'agregarSiniestro'),
    path('verClientes', views.verClientes, name='verClientes')
]