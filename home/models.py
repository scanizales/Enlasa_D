from django.db import models

# Create your models here.

class Project(models.Model):
    """
    Modelo que representa un proyecto
    """
    name= models.CharField(max_length=200, help_text="Ingrese el nombre del proyecto")
    def _str_(self) -> str:
        return self.name 
        
    
class Task (models.Model):
    """
    Modelo que representa un Tarea
    """
    
    title =  models.CharField(max_length=200, help_text="Ingrese el titulo de la tarea")
    descriptions =  models.TextField(help_text="Ingrese la descripcion de la tarea")
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def _str_(self) -> str:
        return self.title + "-" + self.project.name


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


class Cliente(models.Model):
    """
    Modelo que representa un cliente
    """
    TIPO_DOCUMENTO = [ #creación de la enumeración de tipo de documento
        ('CED', 'Cédula'), 
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte')
    ]

    num_documento = models.IntegerField( primary_key = True)
    tipo_documento = models.CharField(max_length = 3, choices = TIPO_DOCUMENTO)
    nombre = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 50)
    ciudad = models.CharField(max_length = 25)
    direccion = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.nomobre



class Poliza(models.Model):
    """
    Modelo que representa una Póliza
    """

    PRIMA = [  #creación de la enumeración de tipo de prima
        ('TRIMESTRA', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]

    MEDIO_PAGO = [ #creación de la enumeración de tipo de medio de pago
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta '),
    ]

    numero = models.CharField(max_length = 5,primary_key = True)
    nombre = models.CharField(max_length = 40)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    prima = models.CharField(max_length = 10, choices = PRIMA)
    medio_pago = models.CharField(max_length = 20, choices = MEDIO_PAGO)
    estado = models.BooleanField()
    aseguradora_id = models.ForeignKey(Aseguradora, on_delete = models.CASCADE)
    cliente_id = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    tipo_seguro_id = models.ForeignKey(Tipo_Seguro, on_delete = models.CASCADE)

    def __str__ (self) -> str:
        return self.nombre


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
        return self.nombre

class  Usuario(models.Model):
    """
    Modelo que representa un Usuario
    """

    TIPO_DOCUMENTO = [ #creación de la enumeración de tipo de documento
        ('CC', 'Cédula'), 
        ('NIT', 'NIT'),
        ('CE', 'Cédula extranjera')
    ]

    ROL = [ #creación de la enumeración de tipo de rol
        ('CLIENTE', 'Cliente'),
        ('GERENTE', 'Gerente'),
        ('ADMINISTRADOR', 'Administrador')
    ]
    
    num_documento = models.IntegerField( primary_key = True)
    tipo_documento = models.CharField(max_length = 3, choices = TIPO_DOCUMENTO)
    rol = models.CharField(max_length = 14, choices = ROL)
    nombre = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 8)

    def __str__ (self) -> str:
       return self.nombre







