from django.shortcuts import get_object_or_404, redirect, render
from Login.models import Paciente
from django.contrib import messages

# Create your views here.
def MostrarPacientes(request):
    if 'nombre_clinico' in request.session:
        nombre_clinico = request.session['nombre_clinico']
        es_admin = request.session.get('es_admin', False)
        paciente = Paciente.objects.all()
        if not paciente.exists():
            messages.error(request, "No hay pacientes registrados")
        return render(request, 'ListaPacientes.html', {'paciente': paciente})
    else:
        return redirect('login')

def EliminarPaciente(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el RUT del paciente a eliminar
        try:
            paciente = get_object_or_404(Paciente, rut=rut)
            paciente.delete()
            messages.success(request, 'Paciente eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el paciente: {e}')
    return redirect('pacientes')  