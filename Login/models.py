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
    genero = models.CharField(max_length=15,null=True)
    telefono = models.CharField(max_length=12)
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


    #aqui vamos con la primera parte del formulario que es la DuracionDelDolor
    curacionDolor = models.CharField(max_length=20) # todos los tipos de botones 
    # como de 3 o 2 btones la idea es manejarlos como como char para que solo reciban
    # el valor y manejar las validaciones con mi propia logica 
    
    caracteristicasDeDolor = models.JSONField()
    # el models.json field es para almacenar datos complejos, como diccionarios 
    #y selecciones multiples, permite seleccionar datos clave ; valor y  optros tipos
    # de nombre y resultado 
    
    #causa del dolor <-------------------------------------------------------> 
    
    causaDolor = models.CharField(max_length=50)
    accidenteLaboral = models.JSONField()
    calidadAtencion = models.TextField(null=True, blank=True)
    opinionProblemaEnfermeda = models.CharField(max_length=20)
    opinionCuraDolor = models.CharField(max_length=20)
    
    
    # Actividades afectadas <------------------------------------------------------>
    dificultadActividad = models.TextField(null=True,blank=True)
    rangoDificultad = models.IntegerField()
    nesesidadDeApoyo = models.BooleanField()
    
    #condiciones de salud <---------------------------------------------------------->
    
    TiposDeEnfermedades = models.JSONField() # aqui manejo todos los checkbox 
    #menciones <------->
    mencionesActividades = models.JSONField()
    
    #esquemaCorporal
    dolorIntensidad = models.JSONField()
    
    IntensidadDolor = models.IntegerField()
    
    #PreguntasMini
    preguntas1 = models.JSONField() #manejar valores si o no 
    #manejar todos los chekbox Seleccionados 
    #¿Que esperas lograr con un mejor manejo del dolor?, seleccione máximo 2 opción.
    preguntas2 = models.JSONField()
    
    
    #preguntas formulario universitario <------------------------------------------------------->  
    pregunta1_nivelDeSalud = models.IntegerField()
    pregunta2_horas_de_sueño_en_promedio = models.CharField(max_length=30)
    pregunta3_frecuencia_De_Suenio = models.CharField(max_length=30)
    pregunta4_opinion_peso_actual = models.CharField(max_length=30)
    pregunta5_ConsumoComidaRapida = models.CharField(max_length=30)
    pregunta6_PorcionesDeFrutas = models.CharField(max_length=30)
    pregunta7_ejercicioDias = models.CharField(max_length=30)
    pregunta8_minutosPorEjercicios = models.CharField(max_length=30)
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    


