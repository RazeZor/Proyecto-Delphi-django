import json
from django.shortcuts import render, get_object_or_404
from Login.models import formularioClinico, Paciente
from django.contrib import messages

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