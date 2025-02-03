import json
from django.shortcuts import render, get_object_or_404
from Login.models import formularioClinico, Paciente,CuestionarioPSFS
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



def RenderizarGROC(request):
    rut = request.GET.get('rut', '')  
    paciente = get_object_or_404(Paciente, rut=rut)

    if not rut:
        messages.error(request, 'No se encuentra ningún paciente registrado')
    
    return render(request, 'GROC.html', {
        
        'rut': rut,
        'paciente':paciente
        
    })
    

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
