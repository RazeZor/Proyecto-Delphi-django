from datetime import datetime
from django.shortcuts import render, redirect
from Login.models import formularioClinico, Clinico, Paciente
from django.contrib import messages
import json


def FormularioInicial(request):
    # Verificar si el usuario tiene sesión activa como clínico
    rut_clinico = request.session.get('rut_clinico')
    if not rut_clinico:
        messages.error(request, 'debe haber un inicio de sesion para estar aqui...')
        return redirect('login')

    try:
        clinico = Clinico.objects.get(rut=rut_clinico)
    except Clinico.DoesNotExist:
        messages.error(request, 'el clinico no esta en el sistema, intenta nuevamente...')
        return redirect('login')

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fechaNacimiento = request.POST.get('fechaNac')
        genero = request.POST.get('genero')
        contacto = request.POST.get('contact')
        cobertura_de_salud = request.POST.get('cobertura')

        paciente, created = Paciente.objects.update_or_create(
            rut=rut,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'fechaNacimiento': fechaNacimiento,
                'genero': genero,
                'contacto': contacto,
                'cobertura_de_salud': cobertura_de_salud,
            }
        )

        formulario = formularioClinico(
    paciente=paciente,
    clinico=clinico,
    fechaCreacion=datetime.now(),
    medicamentos = json.dumps(request.POST.getlist('medicamentos')),
    ## hasta aqui llega la parte de usuarios.
    
    
    ## pagina 2
    duracionDolor=request.POST.get('btnradio1'),
    caracteristicasDeDolor=json.dumps(request.POST.getlist('caracteristicas')),

    ## pagina 3 esquema
    ubicacionDolor = json.dumps(request.POST.getlist('ubicacionDolor')),
    dolorIntensidad= json.dumps(request.POST.getlist('intensidad')),
  
    
    ## pagina 4
    causaDolor=request.POST.get('causaDolor'),
    accidenteLaboral=json.dumps(request.POST.getlist('accidenteLaboral')),
    calidadAtencion=request.POST.get('calidadAtencion'),
    opinionProblemaEnfermeda=request.POST.get('diagnosis'),
    opinionCuraDolor=request.POST.get('cure'),
    #pagina 5
    TiposDeEnfermedades=json.dumps(request.POST.getlist('TiposDeEnfermedades')),

    #pagina 6
    IntensidadDolor=request.POST.get('IntensidadDolor'),
    preguntas1=json.dumps(request.POST.getlist('preguntas1')),
    nesesidadDeApoyo=request.POST.get('support'),
    #pagina 7
    actividades_afectadas = json.dumps(request.POST.getlist('actividades_afectadas')),
    parametros = json.dumps(request.POST.getlist('parametros')),
    
    #pagina8
    pregunta1_nivelDeSalud=request.POST.get('pregunta1_nivelDeSalud'),
    pregunta2_horas_de_sueño_en_promedio=request.POST.get('horas_sueno'),
    pregunta3_frecuencia_De_Suenio=request.POST.get('op3'),
    pregunta4_opinion_peso_actual=request.POST.get('pregunta4_opinion_peso_actual'),
    pregunta5_ConsumoComidaRapida=request.POST.get('op5'),
    pregunta6_PorcionesDeFrutas=request.POST.get('op6'),
    pregunta7_ejercicioDias=request.POST.get('op7'),
    pregunta8_minutosPorEjercicios=request.POST.get('op8'),
    #preguntas de salud mental
    
    proposito = request.POST.get('proposito'),
    red_de_apoyo = request.POST.get('red_de_apoyo'),
    placer_cosas = request.POST.get('placer_cosas'),
    deprimido = request.POST.get('deprimido'),
    ansioso = request.POST.get('ansioso'),
    preocupacion = request.POST.get('preocupacion'),

    #consumo de sustancias
    #nicotica
    NicotinaSiOno = request.POST.get('NicotinaSiOno'),
    condicionNicotina = request.POST.get('frecuenciaNicotina'),
    nicotinaPreocupacion = request.POST.get('preocupacionNicotina'),
    #cigarro
    AlcoholSiOno = request.POST.get('AlcoholSiOno'),
    condicionAlcohol = request.POST.get('frecuenciaAlcohol'),
    AlcoholPreocupacion = request.POST.get('preocupacionAlcohol'),
    #drogas
    drogasSiOno = request.POST.get('drogasSiOno'),
    condicionDrogas = request.POST.get('CantidadDrogras'),
    DrogasPreocupacion = request.POST.get('DrogasPreocupacion'),
    #marihuana
    marihuanaSiOno = request.POST.get('marihuanaSiOno'),
    condicionMarihuana = request.POST.get('frecuenciaMarihuana'),
    marihuanaPreocupacion = request.POST.get('marihuanaPreocupacion'),
    #preguntas de motivacion
    preguntas2=json.dumps(request.POST.getlist('preguntas2')),
    AreasMotivacion = json.dumps(request.POST.getlist('motivacion')),
    motivacion_Salud = request.POST.get('motivacion_Salud')

    )
        formulario.save()
        
        messages.success(request, 'Formulario guardado exitosamente.')
        return redirect('panel')

    return render(request, 'FormularioInicial.html')
def CuerpoHumano(request):
    return render(request, 'CuerpoHumano.html')