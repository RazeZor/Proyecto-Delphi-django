from django.shortcuts import render
from Login.models import Paciente
from django.contrib import messages

# Create your views here.
def MostrarPacientes(request):
    # Obtener la lista actualizada de pacientes
    paciente = Paciente.objects.all()
    if not paciente.exists():
        messages.error(request, "No hay pacientes registrados")
    return render(request, 'ListaPacientes.html', {'paciente': paciente})