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
    curacionDolor=request.POST.get('btnradio1'),
    caracteristicasDeDolor=json.dumps(request.POST.getlist('caracteristicas')),
    causaDolor=request.POST.get('causaDolor'),
    accidenteLaboral=json.dumps(request.POST.getlist('accidenteLaboral')),
    calidadAtencion=request.POST.get('calidadAtencion'),
    opinionProblemaEnfermeda=request.POST.get('diagnosis'),
    opinionCuraDolor=request.POST.get('cure'),
    dificultadActividad=request.POST.get('dificultadActividad'),
    rangoDificultad=int(request.POST.get('rangoDificultad', 0)) if request.POST.get('rangoDificultad') else None,
    nesesidadDeApoyo=request.POST.get('support'),
    TiposDeEnfermedades=json.dumps(request.POST.getlist('TiposDeEnfermedades')),
    mencionesActividades=json.dumps(request.POST.getlist('mencionesActividades')),
    ubicacionDolor = json.dumps(request.POST.getlist('ubicacionDolor')),
    dolorIntensidad= json.dumps(request.POST.getlist('intensidad')),
    DuracionDolor=int(request.POST.get('DuracionDolor', 0)) if request.POST.get('DuracionDolor') else None,
    preguntas1=json.dumps(request.POST.getlist('preguntas1')),
    preguntas2=json.dumps(request.POST.getlist('preguntas2')),
    pregunta1_nivelDeSalud=int(request.POST.get('pregunta1_nivelDeSalud', 0)) if request.POST.get('pregunta1_nivelDeSalud') else None,
    pregunta2_horas_de_sueño_en_promedio=json.dumps(request.POST.getlist('horas_sueno')),
    pregunta3_frecuencia_De_Suenio=json.dumps(request.POST.getlist('op3')),
    pregunta4_opinion_peso_actual=json.dumps(request.POST.getlist('pregunta4_opinion_peso_actual')),
    pregunta5_ConsumoComidaRapida=json.dumps(request.POST.getlist('op5')),
    pregunta6_PorcionesDeFrutas=json.dumps(request.POST.getlist('op6')),
    pregunta7_ejercicioDias=json.dumps(request.POST.getlist('op7')),
    pregunta8_minutosPorEjercicios=json.dumps(request.POST.getlist('op8')),
    medicamentos = json.dumps(request.POST.getlist('medicamentos')),
    medicamento_efectivo = json.dumps(request.POST.getlist('medicamento_efectivo')),
    #preguntas de salud mental
    proposito = int(request.POST.get('proposito'),0),
    red_de_apoyo = int(request.POST.get('red_de_apoyo'),0),
    placer_cosas = int(request.POST.get('placer_cosas'),0),
    deprimido = int(request.POST.get('deprimido'),0),
    ansioso = int(request.POST.get('ansioso'),0),
    preocupacion = int(request.POST.get('preocupacion'),0),
    #consumo de sustancias
    #nicotica
    NicotinaSiOno = request.POST.get('NicotinaSiOno'),
    condicionNicotina = request.POST.get('condicionNicotina'),
    nicotinaPreocupacion = int(request.POST.get('nicotinaPreocupacion'),0),
    #cigarro
    AlcoholSiOno = request.POST.get('alcoholSiOno'),
    condicionAlcohol = request.POST.get('condicionAlcohol'),
    AlcoholPreocupacion = int(request.POST.get('AlcoholPreocuopacion'),0),
    #drogas
    drogasSiOno = request.POST.get('drogasSiOno'),
    condicionDrogas = request.POST.get('condicionDrogas'),
    DrogasPreocupacion = int(request.POST.get('DrogasPreocupacion'),0),
    #marihuana
    marihuanaSiOno = request.POST.get('marihuanaSiOno'),
    condicionMarihuana = request.POST.get('condicionMarihuana'),
    marihuanaPreocupacion = int(request.POST.get('marihuanaPreocupacion'),0),
    #preguntas de motivacion
    AreasMotivacion = json.dumps(request.POST.getlist('motivacion')),
    motivacion_Salud = request.POST.get('motivacion_Salud')
)
        formulario.save()
        
        messages.success(request, 'Formulario guardado exitosamente.')
        return redirect('panel')

    return render(request, 'FormularioInicial.html')
def CuerpoHumano(request):
    return render(request, 'CuerpoHumano.html')