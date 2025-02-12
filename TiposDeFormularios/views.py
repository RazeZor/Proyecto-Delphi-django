import json
from django.shortcuts import render, get_object_or_404,redirect
from Login.models import formularioClinico, Paciente,CuestionarioPSFS,Groc
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

def RenderizarGROC(request):
    rut = request.GET.get('rut', '')
    paciente = get_object_or_404(Paciente, rut=rut)

    # Verificamos si ya existe una evaluación en la tabla Groc para este paciente
    evaluacion_existente = Groc.objects.filter(paciente=paciente).exists()

    # Obtener los puntajes del paciente, si existe una evaluación
    puntajes = []
    if evaluacion_existente:
        # Obtiene los puntajes de la evaluación del paciente
        groc_obj = Groc.objects.get(paciente=paciente)
        puntajes = groc_obj.puntajeGroc  # Esto devuelve una lista de diccionarios
        NotaGroc = groc_obj.NotaGroc  # Asignamos NotaGroc si existe una evaluacion
    else:   
        NotaGroc = "el Paciente No tiene Notas"  # Si no existe la evaluación, asignamos un valor predeterminado

    if request.method == 'POST':
        fecha_creacion = datetime.now().date()
        puntajeGroc = request.POST.get('puntajeGroc')  # Valor único de la escala
        NotaGroc = request.POST.get('nota_adicional')  # Actualizamos NotaGroc con el valor del formulario
        action = request.POST.get('action', '')  # Obtenemos la acción

        # Validar campos
        if not puntajeGroc:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'GROC.html', {'rut': rut, 'paciente': paciente, 'evaluacion_existente': evaluacion_existente, 'puntajes': puntajes, 'NotaGroc': NotaGroc})

        if action == 'guardar':
            # Acción de guardar (si no existe una evaluación anterior)
            Groc.objects.create(
                paciente=paciente,
                fecha_creacion=fecha_creacion,
                NotaGroc=NotaGroc,
                puntajeGroc=[{'puntaje': int(puntajeGroc)}]  # Guardamos el primer puntaje en la lista
            )
            messages.success(request, "Evaluación registrada correctamente.")
            return HttpResponseRedirect(request.get_full_path())  # Recarga la página actual

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
            return HttpResponseRedirect(request.get_full_path())  # Recarga la página actual
        elif action == 'GuardarNota':
            try:
                evaluacion = Groc.objects.get(paciente=paciente)
                evaluacion.NotaGroc = NotaGroc
                evaluacion.save()

                messages.success(request, "Nota actualizada correctamente.")
            except Groc.DoesNotExist:
                messages.error(request, "No se encontró la evaluación para actualizar la nota.")
            
            return HttpResponseRedirect(request.get_full_path())  # Recarga la página actual


    return render(request, 'GROC.html', {
        'rut': rut,
        'paciente': paciente,
        'evaluacion_existente': evaluacion_existente,
        'puntajes': puntajes,
        'NotaGroc': NotaGroc  # Asegúrate de pasar NotaGroc al contexto
    })

def guardar_psfs(request):
    try:
        if request.method == 'POST':
            rut = request.POST.get('rut')
            paciente = get_object_or_404(Paciente, rut=rut)
            action = request.POST.get('action', '')

            # Datos del formulario
            puntaje_actividad_1 = request.POST.getlist('rango1')
            puntaje_actividad_2 = request.POST.getlist('rango2')
            puntaje_actividad_3 = request.POST.getlist('rango3')
            puntajeTotal = request.POST.getlist('total_score')

            if action == 'guardar':
                # Guardar un nuevo cuestionario
                cuestionario = CuestionarioPSFS.objects.create(
                    paciente=paciente,
                    fecha_creacion=datetime.now().date(),
                    puntaje_actividad_1=json.dumps(puntaje_actividad_1),
                    puntaje_actividad_2=json.dumps(puntaje_actividad_2),
                    puntaje_actividad_3=json.dumps(puntaje_actividad_3),
                    puntajeTotal=json.dumps(puntajeTotal),
                )
                cuestionario.save()
            
            elif action == 'actualizar':
                # Actualizar un cuestionario existente sin sobrescribir datos
                cuestionario = CuestionarioPSFS.objects.filter(paciente=paciente).first()
                if cuestionario:
                    # Convertir los JSON en listas para agregar datos sin sobrescribir
                    actividad_1_actual = json.loads(cuestionario.puntaje_actividad_1) if cuestionario.puntaje_actividad_1 else []
                    actividad_2_actual = json.loads(cuestionario.puntaje_actividad_2) if cuestionario.puntaje_actividad_2 else []
                    actividad_3_actual = json.loads(cuestionario.puntaje_actividad_3) if cuestionario.puntaje_actividad_3 else []
                    total_actual = json.loads(cuestionario.puntajeTotal) if cuestionario.puntajeTotal else []

                    # Agregar los nuevos valores sin sobrescribir
                    actividad_1_actual.extend(puntaje_actividad_1)
                    actividad_2_actual.extend(puntaje_actividad_2)
                    actividad_3_actual.extend(puntaje_actividad_3)
                    total_actual.extend(puntajeTotal)

                    # Guardar los datos actualizados
                    cuestionario.puntaje_actividad_1 = json.dumps(actividad_1_actual)
                    cuestionario.puntaje_actividad_2 = json.dumps(actividad_2_actual)
                    cuestionario.puntaje_actividad_3 = json.dumps(actividad_3_actual)
                    cuestionario.puntajeTotal = json.dumps(total_actual)
                    cuestionario.save()
                else:
                    return HttpResponse('No hay un cuestionario existente para actualizar.', status=404)

            return redirect('historialClinico')

        return HttpResponse('Método no permitido', status=405)
    except ValueError:
        return HttpResponse('YA EXISTEN DATOS ', status=404)
    except:
        return HttpResponse('YA EXISTEN DATOS ', status=404)

def RenderizarPSFS(request):

    rut = request.GET.get('rut', '')  
    paciente = get_object_or_404(Paciente, rut=rut)
    formularios = formularioClinico.objects.filter(paciente=paciente) # para mostrar las 3 Actividades Del
    #Fomulario Inicial
    cuestionario = CuestionarioPSFS.objects.filter(paciente=paciente).first()
    evaluacion_existente = CuestionarioPSFS.objects.filter(paciente=paciente).exists()
    nota = cuestionario.NotaCuestionarioPSFS
    if cuestionario:
        puntajes_actividad_1 = json.loads(cuestionario.puntaje_actividad_1) if cuestionario.puntaje_actividad_1 else []
        puntajes_actividad_2 = json.loads(cuestionario.puntaje_actividad_2) if cuestionario.puntaje_actividad_2 else []
        puntajes_actividad_3 = json.loads(cuestionario.puntaje_actividad_3) if cuestionario.puntaje_actividad_3 else []
        puntajes_total = json.loads(cuestionario.puntajeTotal) if cuestionario.puntajeTotal else []

        sesiones = []
        for i in range(len(puntajes_actividad_1)):
            sesiones.append({
                "sesion": i + 1,
                "actividad_1": puntajes_actividad_1[i] if i < len(puntajes_actividad_1) else "-",
                "actividad_2": puntajes_actividad_2[i] if i < len(puntajes_actividad_2) else "-",
                "actividad_3": puntajes_actividad_3[i] if i < len(puntajes_actividad_3) else "-",
                "total": puntajes_total[i] if i < len(puntajes_total) else "-",
            })
    else:
        sesiones = []

    if formularios.exists():
        formulario = formularios.first()  
        actividades = json.loads(formulario.actividades_afectadas) 
        
        actividad1 = actividades[0] if len(actividades) > 0 else ''
        actividad2 = actividades[1] if len(actividades) > 1 else ''
        actividad3 = actividades[2] if len(actividades) > 2 else ''
    else:
        actividad1 = actividad2 = actividad3 = ''

    return render(request, 'CuestionarioPSFS.html', {
        'rut': rut, 
        'actividad1': actividad1,
        'actividad2': actividad2,
        'actividad3': actividad3,
        'sesiones': sesiones,
        'evaluacion_existente':evaluacion_existente,
        'nota':nota
    })

def GuardarNota(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        notaPSFS = request.POST.get('notes')
        paciente = get_object_or_404(Paciente, rut=rut)
        EvaluacionExistente = CuestionarioPSFS.objects.filter(paciente=paciente).first()
        
        if EvaluacionExistente:
            EvaluacionExistente.NotaCuestionarioPSFS = notaPSFS  # Asignación correcta
            EvaluacionExistente.save()
            messages.success(request, "Nota actualizada correctamente.")
            return redirect('historialClinico')
        else:
            return HttpResponse("Ha ocurrido un error inesperado", status=405)
    else:
        return HttpResponse("No cargaron bien los datos", status=405)
