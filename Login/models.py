from django.db import models

# Modelo Clínico: Representa un clínico en el sistema.
class Clinico(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)  # Clave primaria única
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    # Relación muchos a muchos con pacientes
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
    # Relación uno a uno con formulario inicial
    formularioIni = models.OneToOneField(
        'FormularioInicial',
        on_delete=models.CASCADE,  # Elimina el formulario si se elimina el paciente
        related_name="paciente"
    )

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'


# Modelo FormularioInicial: Representa un formulario inicial único para cada paciente.
class FormularioInicial(models.Model):
    id = models.AutoField(primary_key=True)  # ID único para cada formulario
    # Campos del formulario
    pregunta1 = models.CharField(max_length=50)
    pregunta2 = models.CharField(max_length=50)
    pregunta3 = models.CharField(max_length=50)
    pregunta4 = models.CharField(max_length=50)
    pregunta5 = models.CharField(max_length=50)
    pregunta6 = models.CharField(max_length=50)
    pregunta7 = models.CharField(max_length=50)
    pregunta8 = models.CharField(max_length=50)
    pregunta9 = models.CharField(max_length=50)
    pregunta10 = models.CharField(max_length=50)
    pregunta11 = models.CharField(max_length=50)
    pregunta12 = models.CharField(max_length=50)
    pregunta13 = models.CharField(max_length=50)
    pregunta14 = models.CharField(max_length=50)

    def __str__(self):
        return f'Formulario {self.id}'
