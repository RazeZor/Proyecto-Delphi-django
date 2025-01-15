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
    apellido = models.CharField(max_length=50,null=False)
    fechaNacimiento = models.DateTimeField(null=True)
    genero = models.CharField(max_length=15,null=True)
    contacto = models.CharField(max_length=12)
    cobertura_de_salud = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'

#charfield  : son los varchar qe sabemos de sql

# textField : es un atributo que recibe una cantidad gigante de strings 

# jsonField : es un tipo de dato tipo diccionario que recibe valores complejos,
    #como respuestas multiples (chekbox entre otros)
    
#IntegerField : recibe valores enteros  

#.BooleanField : recibe respuesta boolean true or false 

class formularioClinico(models.Model):
    #ejectuo las tablas foraneas el cual 1 formulario es de 1 paciente 
    #y asegura que ese clinico realizo ese formulario 
    id= models.AutoField(primary_key=True,unique=True)
    paciente = models.OneToOneField('Paciente', on_delete=models.CASCADE, related_name='formulario')
    clinico = models.ForeignKey('Clinico', on_delete=models.CASCADE, related_name='formularios')
    fechaCreacion = models.DateTimeField(auto_now_add=True) 
    curacionDolor = models.CharField(max_length=20,null=True, blank=True) # todos los tipos de botones 
    caracteristicasDeDolor = models.JSONField()
    causaDolor = models.CharField(max_length=50,null=True, blank=True)
    accidenteLaboral = models.JSONField(null=True, blank=True)
    calidadAtencion = models.TextField(null=True, blank=True)
    opinionProblemaEnfermeda = models.CharField(max_length=20,null=True, blank=True)
    opinionCuraDolor = models.CharField(max_length=20,null=True, blank=True)
    dificultadActividad = models.TextField(null=True,blank=True)
    rangoDificultad = models.IntegerField(null=True, blank=True)
    nesesidadDeApoyo = models.CharField(max_length=20,null=True, blank=True)
    TiposDeEnfermedades = models.JSONField(null=True, blank=True) # aqui manejo todos los checkbox 
    mencionesActividades = models.JSONField(null=True, blank=True)
    ubicacionDolor= models.JSONField(null=True,blank=True)
    dolorIntensidad = models.JSONField(null=True, blank=True)
    DuracionDolor = models.IntegerField(null=True, blank=True)
    preguntas1 = models.JSONField(null=True, blank=True) 
    preguntas2 = models.JSONField(null=True, blank=True)
    pregunta1_nivelDeSalud = models.IntegerField(null=True, blank=True)
    pregunta2_horas_de_sueño_en_promedio = models.JSONField(null=True, blank=True)
    pregunta3_frecuencia_De_Suenio = models.JSONField(null=True, blank=True)
    pregunta4_opinion_peso_actual = models.JSONField(null=True, blank=True)
    pregunta5_ConsumoComidaRapida = models.JSONField(null=True, blank=True)
    pregunta6_PorcionesDeFrutas = models.JSONField(null=True, blank=True)
    pregunta7_ejercicioDias = models.JSONField(null=True, blank=True)
    pregunta8_minutosPorEjercicios = models.JSONField(null=True, blank=True)
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    


