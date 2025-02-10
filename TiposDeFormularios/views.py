from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from Login.models import formularioClinico, Paciente,CuestionarioPSFS,Groc
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json

def RenderizarPSFS(request):
    rut = request.GET.get('rut', '')  
    paciente = get_object_or_404(Paciente, rut=rut)
    formularios = formularioClinico.objects.filter(paciente=paciente)
    
    if formularios.exists():
        formulario = formularios.first()  
        actividades = json.loads(formulario.actividades_afectadas) 
        
        # Asignar las actividades a variables
        actividad1 = actividades[0] if len(actividades) > 0 else ''
        actividad2 = actividades[1] if len(actividades) > 1 else ''
        actividad3 = actividades[2] if len(actividades) > 2 else ''
        
    else:
        actividad1 = actividad2 = actividad3 = ''
    
    return render(request, 'PSFS.html', {
        'rut': rut, 
        'actividad1': actividad1,
        'actividad2': actividad2,
        'actividad3': actividad3,
    })


from datetime import datetime

def RenderizarGROC(request):
    rut = request.GET.get('rut', '')  
    paciente = get_object_or_404(Paciente, rut=rut)

    # Verificamos si ya existe una evaluación en la tabla Groc para este paciente
    evaluacion_existente = Groc.objects.filter(paciente=paciente).exists()

    if request.method == 'POST':
        fecha_creacion = datetime.now().date()  # Usamos solo la fecha (sin la hora)
        puntajeGroc = request.POST.get('puntajeGroc')  # Valor único de la escala
        action = request.POST.get('action', '')  # Obtenemos la acción

        # Validar campos
        if not puntajeGroc:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'GROC.html', {'rut': rut, 'paciente': paciente, 'evaluacion_existente': evaluacion_existente})

        if action == 'guardar':
            # Acción de guardar (si no existe una evaluación anterior)
            Groc.objects.create(
                paciente=paciente,
                fecha_creacion=fecha_creacion,
                puntajeGroc=[{'puntaje': int(puntajeGroc)}]  # Guardamos el primer puntaje en la lista
            )
            messages.success(request, "Evaluación registrada correctamente.")
            return redirect('historialClinico')

        elif action == 'actualizar':
            try:
                evaluacion = Groc.objects.get(paciente=paciente)
                
                if isinstance(evaluacion.puntajeGroc, list):
                    evaluacion.puntajeGroc.append({'puntaje': int(puntajeGroc)})
                else:
                    evaluacion.puntajeGroc = [{'puntaje': int(puntajeGroc)}]

                evaluacion.save()
                messages.success(request, "Evaluación actualizada correctamente.")
            except Groc.DoesNotExist:
                messages.error(request, "No se encontró la evaluación para actualizar.")
            return redirect('historialClinico')

    return render(request, 'GROC.html', {'rut': rut, 'paciente': paciente, 'evaluacion_existente': evaluacion_existente})

def guardar_psfs(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        date = request.POST.get('date')
        actividades = request.POST.getlist('actividad[]')

        # Obtén el paciente usando el RUT
        paciente = get_object_or_404(Paciente, rut=rut)

        # Crea el cuestionario PSFS
        cuestionario = CuestionarioPSFS.objects.create(
            paciente=paciente,
            fecha_creacion=date
        )

        for i, actividad in enumerate(actividades):
            scores = request.POST.getlist(f'score_actividad{i + 1}[]')  
            puntaje_total = sum(int(score) for score in scores)  

            if i == 0:
                cuestionario.puntaje_actividad_1 = puntaje_total
            elif i == 1:
                cuestionario.puntaje_actividad_2 = puntaje_total
            elif i == 2:
                cuestionario.puntaje_actividad_3 = puntaje_total

        cuestionario.save()

        return redirect('panel')  
    
    return HttpResponse('Método no permitido', status=405)
