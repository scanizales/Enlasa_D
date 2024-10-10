from django.contrib import admin
from .models import Project, Task, Aseguradora, Tipo_Seguro, Cliente, Poliza, Siniestro, Usuario

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Aseguradora)
admin.site.register(Tipo_Seguro)
admin.site.register(Cliente)
admin.site.register(Poliza)
admin.site.register(Usuario)
