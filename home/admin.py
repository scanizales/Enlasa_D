from django.contrib import admin
from .models import  Aseguradora, Tipo_Seguro, Seguro, Cliente, Poliza, Siniestro, Usuario, Beneficiario, Policy_Beneficiary

# Register your models here.
admin.site.register(Aseguradora)
admin.site.register(Tipo_Seguro)
admin.site.register(Policy_Beneficiary)
admin.site.register(Seguro)
admin.site.register(Cliente)
admin.site.register(Poliza)
admin.site.register(Beneficiario)
admin.site.register(Siniestro)
admin.site.register(Usuario)
