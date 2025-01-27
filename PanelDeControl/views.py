import json
from django.shortcuts import render, redirect
from Login.models import Paciente, formularioClinico,tiempo
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
    
def cerrar_sesion(request):
    # Elimina todos los datos de la sesión
    request.session.flush()
    
    # Redirige al login (o a cualquier otra página que desees)
    return redirect('login')  # Asegúrate de que 'login' sea el nombre de tu URL de login

def VerFichaPacientes(request):
    if 'nombre_clinico' not in request.session:
        return redirect('login')
    
    nombre_clinico = request.session['nombre_clinico']
    rut = request.GET.get('rut', None)
    context = {'nombre_clinico': nombre_clinico}

    if rut:
        try:
            paciente = Paciente.objects.get(rut=rut)
            formulario = formularioClinico.objects.get(paciente=paciente)

            mensajeDuracionDolor = evaluar_duracion_dolor(formulario.duracionDolor)
            mensajeOpinion = evaluar_opinion(formulario.opinionProblemaEnfermeda, formulario.opinionCuraDolor)
            mensajeApoyo = evaluar_necesidad_apoyo(formulario.nesesidadDeApoyo)

            respuestas = formulario.parametros
            mensajeEVPER = Respuesta_evitativo_persistente(json.loads(respuestas)) 
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
                mensajeDuracionDolor=mensajeDuracionDolor,
                mensajeOpinion=mensajeOpinion,
                mensajeApoyo=mensajeApoyo,
                mensajeEVPER=mensajeEVPER,
                ubicacion_intensidad=ubicacion_intensidad_list
            )


            context['informe'] = informe
            context['encontrado'] = True

        except (Paciente.DoesNotExist, formularioClinico.DoesNotExist):
            context['encontrado'] = False
            context['mensaje'] = "No se encontró el paciente o su formulario clínico"

    return render(request, 'FichaPacientes.html', context)

def evaluar_duracion_dolor(duracionDolor):
    condicionduracionDolor = 'mas de 6 meses'
    if duracionDolor == condicionduracionDolor:
        return (
            '<h6 style="color: red;">El paciente reporta un dolor de más de 6 meses. Se le sugiere al clinico utilizar la escala DN4.</h6>'
        )
    else:
        return ("<h4>No hay consejos.</h4>")

def evaluar_opinion(opinionEnfermedad, opinioncuraDolor):
    puntaje = 0
    
    if opinioncuraDolor == 'no':
        puntaje += 2
    if opinionEnfermedad == 'si':
        puntaje += 1

    if puntaje > 2:
        return (
            '<h6 style="color: red;">Se le sugiere al médico utilizar la escala PCS ---> creencias: aceptación de dolor <--- CPAQ</h6>'
        )
    elif puntaje == 2:
        return (
            '<h6 style="color: red;">Creencias: aceptación de dolor <--- CPAQ</h6>'
        )
    elif puntaje == 1:
        return (
            '<h6 style="color: red;">Se le sugiere al médico utilizar la escala PCS ---> creencias</h6>'
        )
    
    return ''

def evaluar_necesidad_apoyo(apoyo):
    if apoyo == 'si':
        return (
            '<h6 style="color: red;">El paciente pide apoyo para ansiedad o depresión. Se sugiere derivar a un especialista (psicólogo, psiquiatra).</h6>'
        )
    

    return ('')




def Respuesta_evitativo_persistente(respuestas):
    EVITATIVAS = "evitativo"
    PERSISTENTES = "persistente"
    evitativo = 0
    persistente = 0

    for respuesta in respuestas:
        if respuesta.strip().lower() == EVITATIVAS:
            evitativo += 1
        elif respuesta.strip().lower() == PERSISTENTES:
            persistente += 1

    if evitativo > persistente:
        return '<h6 style="color: red;">Tiene una conducta de evitación</h6>'
    elif persistente > evitativo:
        return '<h6 style="color: red;">Tiene una conducta persistente</h6>'
    else:
        return '<h6 style="color: orange;">Tiene una conducta equilibrada</h6>'
    
    

