from django.db import models

# Modelo Clínico: Representa un clínico en el sistema.
class Clinico(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)  # Clave primaria única
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50,default='default_profession')
    contraseña = models.CharField(max_length=50, default='default_password')
    pacientes = models.ManyToManyField('Paciente', related_name='clinicos')

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'


# Modelo Paciente: Representa a un paciente en el sistema.
class Paciente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)  # Clave primaria única
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1)
    telefono = models.CharField(max_length=12)
    cobertura_de_salud = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'


