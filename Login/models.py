from django.db import models


# Modelo Clínico: Representa un clínico en el sistema.
class Clinico(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)  # Clave primaria única
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50, default='default_profession')
    contraseña = models.CharField(max_length=50, default='default_password')
    EsAdmin = models.BooleanField(default=False)
    pacientes = models.ManyToManyField('Paciente', related_name='clinicos')
    EsAdmin = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'


# Modelo Paciente: Representa a un paciente en el sistema.
class Paciente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)  # Clave primaria única
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50,null=False)
    fechaNacimiento = models.DateField(null=True)
    genero = models.CharField(max_length=15,null=True)
    contacto = models.CharField(max_length=12)
    cobertura_de_salud = models.CharField(max_length=50)
    trabajo = models.CharField(max_length=50, null=True, blank=True)
    profesion = models.CharField(max_length=50, default='Sin profesion')
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
    medicamentos = models.JSONField(null=True,blank=True) #listo
    #hasta aqui la pagina 1
    #pagina2
    duracionDolor = models.CharField(max_length=20,null=True, blank=True) # todos los tipos de botones 
    caracteristicasDeDolor = models.JSONField()
    
    
    #pagina3
    ubicacionDolor= models.JSONField(null=True,blank=True)
    dolorIntensidad = models.JSONField(null=True, blank=True)
    
    #pagina4
    causaDolor = models.CharField(max_length=50,null=True, blank=True)
    accidenteLaboral = models.JSONField(null=True, blank=True)
    calidadAtencion = models.TextField(null=True, blank=True)
    opinionProblemaEnfermeda = models.CharField(max_length=20,null=True, blank=True)
    opinionCuraDolor = models.CharField(max_length=20,null=True, blank=True)
    
    
    #pagina 5
    TiposDeEnfermedades = models.JSONField(null=True, blank=True)

    #pagina6
    IntensidadDolor = models.TextField(null=True, blank=True)
    preguntas1 = models.JSONField(null=True, blank=True)
    nesesidadDeApoyo = models.CharField(max_length=20,null=True, blank=True)
    
    
    #pagina7 
    actividades_afectadas = models.JSONField(null=True,blank=True)
    parametros = models.JSONField(null=True, blank=True)
    
    #pagina 8
    pregunta1_nivelDeSalud = models.TextField(null=True, blank=True)
    pregunta2_horas_de_sueño_en_promedio = models.TextField(null=True, blank=True)
    pregunta3_frecuencia_De_Suenio = models.TextField(null=True, blank=True)
    pregunta4_opinion_peso_actual = models.TextField(null=True, blank=True)
    #pagina 9
    pregunta5_ConsumoComidaRapida = models.TextField(null=True, blank=True)
    pregunta6_PorcionesDeFrutas = models.TextField(null=True, blank=True)
    pregunta7_ejercicioDias = models.TextField(null=True, blank=True)
    pregunta8_minutosPorEjercicios = models.TextField(null=True, blank=True)
    #pagina 9
    proposito = models.TextField(null=True,blank=True)
    red_de_apoyo = models.TextField(null=True,blank=True)
    placer_cosas = models.TextField(null=True,blank=True)
    deprimido = models.TextField(null=True,blank=True)
    ansioso = models.TextField(null=True,blank=True)
    preocupacion = models.TextField(null=True,blank=True)
    
    #pag 10
    NicotinaSiOno = models.JSONField(blank=True,null=True)
    condicionNicotina =  models.TextField(null=True,blank=True)
    nicotinaPreocupacion = models.TextField(null=True,blank=True)
    
    AlcoholSiOno = models.JSONField(blank=True,null=True)
    condicionAlcohol =  models.TextField(null=True,blank=True)
    AlcoholPreocupacion = models.TextField(null=True,blank=True)
    
    #pag 11
    drogasSiOno = models.JSONField(blank=True,null=True) 
    condicionDrogas =  models.TextField(null=True,blank=True)
    DrogasPreocupacion = models.TextField(null=True,blank=True)
    
    marihuanaSiOno = models.JSONField(blank=True,null=True)
    condicionMarihuana =  models.TextField(null=True,blank=True)
    marihuanaPreocupacion = models.TextField(null=True,blank=True)


    
    #motivacion 
    preguntas2 = models.JSONField(null=True, blank=True)
    AreasMotivacion = models.JSONField(null=True,blank=True)
    motivacion_Salud = models.TextField(null=True,blank=True)
    
class tiempo(models.Model):
    duracion = models.DurationField()
    
    def __str__(self):
        return f'tiempo = {self.duracion}'

    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    


