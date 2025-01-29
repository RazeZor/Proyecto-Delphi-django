from django.shortcuts import render
from Login.models import Paciente
from django.contrib import messages

def RenderizarPSFS(request):
    pacientes = Paciente.objects.all()  

    if not pacientes:
        messages.error(request, 'No se encuentra ningún paciente registrado')
    
    return render(request, 'PSFS.html', {'pacientes': pacientes})