import json
from django.shortcuts import get_object_or_404, render, redirect
from Login.models import Paciente, formularioClinico,tiempo,Notas
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import time 

def panel(request):
    if 'nombre_clinico' in request.session:
        nombre_clinico = request.session['nombre_clinico']
        es_admin = request.session.get('es_admin', False)

        tiempos = tiempo.objects.all()

        if tiempos.exists():
            total_duracion = sum((t.duracion for t in tiempos), timedelta())
            promedio_duracion = total_duracion / len(tiempos)

            horas, resto = divmod(promedio_duracion.total_seconds(), 3600)
            minutos, segundos = divmod(resto, 60)
            promedio_formateado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
        else:
            promedio_formateado = "00:00:00"  
        
        pacientes = Paciente.objects.all()
        numeroPaciente = 0
        for paciente in pacientes:
            numeroPaciente = numeroPaciente+1
            
        return render(request, 'panel.html', {
            'nombre_clinico': nombre_clinico,
            'es_admin': es_admin,
            'promedio_formateado': promedio_formateado,
            'numeroPaciente': numeroPaciente
        })
    else:
        return redirect('login')
    
#def RenderizarDatosPaciente(request):
    #pacientes = Paciente.objects.all()
    #return render(request, 'panel.html', {'pacientes': pacientes})    


def cerrar_sesion(request):
    # Elimina todos los datos de la sesión
    request.session.flush()
    
    # Redirige al login (o a cualquier otra página que desees)
    return redirect('login')  # Asegúrate de que 'login' sea el nombre de tu URL de login


def HistorialClinico(request):
    paciente = None
    error = None

    if request.method == 'POST':
        rut = request.POST.get('rutsito')
        try:
            paciente = Paciente.objects.get(rut=rut)
        except Paciente.DoesNotExist:
            error = "No se encontró ningún paciente con ese RUT."

    return render(request, 'HistorialClinicoPacientes.html', {'paciente': paciente, 'error': error})

def GuardarNotaPaciente(request):
    paciente = None
    error = None
    nota_existente = None

    if request.method == 'POST':
        rut = request.POST.get('rutsito')
        nota_texto = request.POST.get('nota')
        try:
            paciente = Paciente.objects.get(rut=rut)

            # Si ya existe una nota para este paciente, obtenla, si no, créala
            nota_existente, created = Notas.objects.get_or_create(paciente=paciente)
            if nota_texto:  
                nota_existente.notas = nota_texto
                nota_existente.save()

        except Paciente.DoesNotExist:
            error = "No se encontró ningún paciente con ese RUT."
    if paciente:
        nota_existente = Notas.objects.filter(paciente=paciente).first()

    return render(request, 'HistorialClinicoPacientes.html', {
        'paciente': paciente,
        'error': error,
        'nota': nota_existente.notas if nota_existente else ''
    })



def VerInformePacientes(request):
    if 'nombre_clinico' not in request.session:
        return redirect('login')
    
    nombre_clinico = request.session['nombre_clinico']
    rut = request.GET.get('rut', None)
    context = {'nombre_clinico': nombre_clinico}

    if rut:
        try:
            paciente = Paciente.objects.get(rut=rut)
            formulario = formularioClinico.objects.get(paciente=paciente)
            #escala Semaforo Integrada
            semaforo = json.loads(formulario.preguntas1)
            mensajeSemaforo = EscalaSemaforo(semaforo)
            
            #mensaje apoyo 
            mensajeApoyo = evaluar_necesidad_apoyo(formulario.nesesidadDeApoyo)
            
            #mensaje caracteristicas de dolor
            caracteristicasDolor = json.loads(formulario.caracteristicasDeDolor)
            MensajecaracteristicasDolor = Neuropaticas(caracteristicasDolor)

            #mensaje fibromialgia
            condicionesSalud1 = json.loads(formulario.TiposDeEnfermedades)
            MensajeCondicionesSalud = condicionesSalud(condicionesSalud1)

           
            #uso importante de JsonLoad, esta es la unica manera
            #que carguen bien las respuestas Json De el Atribuo JsonField de la base de Datos
            
            # el cuerpo humano Bien mostrado 

            ubicacionDolor = json.loads(formulario.ubicacionDolor)
            intensidadDolor = json.loads(formulario.dolorIntensidad)
            
            ubicacion_intensidad_list = ""


            min_len = min(len(ubicacionDolor), len(intensidadDolor))
            for i in range(min_len):
                ubicacion = ubicacionDolor[i]
                intensidad = intensidadDolor[i]
                ubicacion_intensidad_list += f"<li><strong>{ubicacion}:</strong> {intensidad}</li>\n"

            if len(ubicacionDolor) != len(intensidadDolor):
                ubicacion_intensidad_list += "<li><strong>Error:</strong> Las listas no coinciden en longitud</li>\n"

                
            with open('informe/templates/informe.html', 'r', encoding='utf-8') as template_file:
                informe_template = template_file.read()

            informe = informe_template.format(
                paciente=paciente,
                formulario=formulario,
                mensajeApoyo=mensajeApoyo,
                ubicacion_intensidad=ubicacion_intensidad_list,
                mensajeSemaforo=mensajeSemaforo,
                MensajecaracteristicasDolor=MensajecaracteristicasDolor,
                MensajeCondicionesSalud=MensajeCondicionesSalud,
            )


            context['informe'] = informe
            context['encontrado'] = True

        except (Paciente.DoesNotExist, formularioClinico.DoesNotExist):
            context['encontrado'] = False
            context['mensaje'] = "No se encontró el paciente o su formulario clínico"

    return render(request, 'FichaPacientes.html', context)




def evaluar_necesidad_apoyo(apoyo):
    if apoyo == 'si':
        return (
            '<div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; border: 1px solid #f5c6cb;">'
            '<h6>El paciente pide apoyo para ansiedad o depresión. Se sugiere derivar a un especialista (psicólogo, psiquiatra).</h6>'
            '</div>'
        )
    return ('')

def EscalaSemaforo(preguntas1):
    score = 0
    RESPUESTA = 'si'
    MODERADO = 'moderado'
    MUCHO = 'mucho'
    EXTREMO = 'extremo'
    
    for preguntas in preguntas1:
        if preguntas == RESPUESTA:
            score += 1
        if preguntas.strip().lower() in [MODERADO, MUCHO, EXTREMO]:
            score += 1

    if score <= 3:
        return (
            '<div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; border: 1px solid #c3e6cb;">'
            '<label>El paciente tiene un riesgo bajo, se recomienda educar y tranquilizar al paciente, diciendo que el diagnóstico es bueno.</label>'
            '</div>'
        )
    elif score >= 4 and score <= 7:
        return (
            '<div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; border: 1px solid #ffeeba;">'
            '<label>El paciente tiene un riesgo medio en la escala Scrining Semaforo, evaluar si necesitará ayuda de otro profesional.</label>'
            '</div>'
        )
    elif score >= 8:
        return (
            '<div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; border: 1px solid #f5c6cb;">'
            '<p>El paciente tiene un riesgo alto, se recomienda tratamiento interdisciplinario.</p>'
            '</div>'
        )
        
def Neuropaticas(caracteristicasDolor):
    for caracteristicas in caracteristicasDolor:
        if caracteristicas == "ardiente" or caracteristicas == "corriente" or caracteristicas == "adormecimiento" or caracteristicas == "Hormigueo":
            return (
                '<div style="background-color: #fff3cd; color: #155724; padding: 15px; border-radius: 5px; border: 1px solid #c3e6cb;">'
                '<label>El paciente tiene un dolor neuropático se recomienda al Clinico Usar la Escala DN4 o TSK-11 </label>'
                '</div>'
            )
    return ('')


def condicionesSalud(condicionesSalud):
    for condicion in condicionesSalud:
        if condicion == "Fibromialgia":
            return (
                '<div style="background-color: #fff3cd; color: #155724; padding: 15px; border-radius: 5px; border: 1px solid #c3e6cb;">'
                '<label>El paciente tiene una enfermedad de Fibromialgia, se recomienda uso de formulario para Fibromialgia</label>'
                '</div>'
            )
    return ('')



        






    


