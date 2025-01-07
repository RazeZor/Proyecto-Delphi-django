from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from Login.models import Clinico
def AgregarClinico(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        profesion = request.POST['profesion']
        contraseña = request.POST['contraseña']
        
        try:
            clinico = Clinico(rut=rut, nombre=nombre, apellido=apellido,profesion=profesion, contraseña=contraseña)
            clinico.save()
            return redirect('ver')
            
            
        except Exception as e:
            messages.error(request, f'Error al agregar el clínico: {e}')
    return render(request, 'AgregarClinico.html')


def VerClinicos(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el rut del clínico a eliminar
        if rut:
            clinico = Clinico.objects.get(rut=rut)  # Obtener el clínico a eliminar
            clinico.delete()  # Eliminar al clínico
            redirect('VerClinicos.html')
            

    # Obtener la lista actualizada de clínicos
    clinicos = Clinico.objects.all()
    return render(request, 'VerClinicos.html', {'clinicos': clinicos})

    
    
