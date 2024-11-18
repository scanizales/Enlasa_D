from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy 

class Aseguradora(models.Model):

    """
    Modelo que representa una aseguradora
    """

    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 10)
    direccion = models.CharField(max_length = 30)

    def _str_(self) -> str:
        return self.nombre


class Tipo_Seguro(models.Model):

    """
    Modelo que representa un tipo de seguro
    """

    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60)

    def _str_(self) -> str:
        return self.nombre

class Seguro(models.Model):

    """
    Modelo que representa un seguro
    """

    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60)
    tipo_seguro_id =  models.ForeignKey(Tipo_Seguro, on_delete=models.CASCADE)

    def _str_(self) -> str:
        return self.nombre

class Cliente(models.Model):
    """
    Modelo que representa un cliente
    """
    TIPO_DOCUMENTO = [ #creación de la enumeración de tipo de documento
        ('CC', 'Cédula'), 
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
        ('CE', 'Cédula de extranjería'),
    ]

    num_documento = models.IntegerField( primary_key = True)
    tipo_documento = models.CharField(max_length = 3, choices = TIPO_DOCUMENTO)
    nombre = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 50, null = True)
    celular = models.CharField(max_length = 50, default = 1)
    ciudad = models.CharField(max_length = 25)
    direccion = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.nombre



class Poliza(models.Model):
    """
    Modelo que representa una Póliza
    """

    PRIMA = [  #creación de la enumeración de tipo de prima
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]

    MEDIO_PAGO = [ #creación de la enumeración de tipo de medio de pago
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta '),
    ]
    id = models.AutoField(primary_key = True)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    prima = models.CharField(max_length = 10, choices = PRIMA)
    medio_pago = models.CharField(max_length = 20, choices = MEDIO_PAGO)
    estado = models.BooleanField()
    aseguradora_id = models.ForeignKey(Aseguradora, on_delete = models.CASCADE)
    cliente_id = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    seguro_id = models.ForeignKey(Seguro, on_delete = models.CASCADE)

    def __str__ (self) -> str:
        return self.nombre


class Beneficiario(models.Model):
    """
    Modelo que representa un cliente
    """
    TIPO_DOCUMENTO = [ #creación de la enumeración de tipo de documento
        ('CED', 'Cédula'), 
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte')
    ]

    num_documento = models.IntegerField( primary_key = True)
    nombre = models.CharField(max_length = 50)
    tipo_documento = models.CharField(max_length = 3, choices = TIPO_DOCUMENTO)

    def __str__(self) -> str:
        return self.nombre


class Poliza_Beneficiario(models.Model):
    """
    Modelo que representa relación entre póliza y beneficiario
    """

    id = models.AutoField(primary_key = True)
    poliza_id = models.ForeignKey(Poliza, on_delete = models.CASCADE)
    beneficiario_id = models.ForeignKey(Beneficiario, on_delete = models.CASCADE)

    def __str__ (self) -> str:
        return self.id


class Siniestro(models.Model):
    """
    Modelo que representa un siniestro
    """

    ESTADO = [ #creación de la enumeración de tipo de estado del siniestro
        ('REPORTADO', 'Reportado'),
        ('EN_PROCESO', 'En proceso'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('RESUELTO', 'Resuelto'),
    ]

    fecha = models.DateField()
    descripcion = models.TextField()
    estado = models.CharField(max_length = 15, choices= ESTADO)
    poliza_id = models.ForeignKey(Poliza, on_delete = models.CASCADE)

    def __str__ (self) -> str:
        return self.descripcion

class UsuarioManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(num_documento = username)

    def create_user(self, num_documento, password, **extra_fields):
        if not num_documento:
            raise ValueError(('El número de documento es requerido.'))
        user = self.model(num_documento = num_documento, **extra_fields)
        user.set_password(password)
        user.save()
        return user
      

class  Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo que representa un Usuario
    """

    ROL = [ #creación de la enumeración de tipo de rol
        ('CLIENTE', 'Cliente'),
        ('GERENTE', 'Gerente'),
        ('ADMINISTRADOR', 'Administrador')
    ]
    
    num_documento = models.IntegerField( primary_key = True, unique=True)
    rol = models.CharField(max_length = 14, choices = ROL)
    nombre = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    password = models.CharField(max_length = 8)

    REQUIRED_FIELDS = ['rol']
    USERNAME_FIELD = 'num_documento'

    objects = UsuarioManager()

    def __str__ (self) -> str:
       return self.nombre
















