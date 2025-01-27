from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from Login.models import Clinico
from django.contrib import messages
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
            messages.success(request, 'Clínico Agregado Exitosamente')
            
            return redirect('ver')
            
            
        except Exception as e:
            messages.error(request, f'Error al agregar el clínico: {e}')
    return render(request, 'AgregarClinico.html')


def VerClinicos(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el rut del clínico a eliminar
        if rut:
            clinico = Clinico.objects.get(rut=rut)
            clinico.delete()  # Eliminar al clínico
            messages.success(request, 'Clínico eliminado exitosamente.')
            return redirect('ver')  # Redirige después de eliminar

    # Obtener la lista actualizada de clínicos
    clinicos = Clinico.objects.all()
    return render(request, 'VerClinicos.html', {'clinicos': clinicos})

def EditarClinicos(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        profesion = request.POST['profesion']

        try:
            clinico = get_object_or_404(Clinico, rut=rut)
            clinico.nombre = nombre
            clinico.apellido = apellido
            clinico.profesion = profesion
            clinico.save()
            messages.success(request, 'Clínico editado exitosamente.')
            # Enviar el mensaje usando messages.success
          

        except Exception as e:
            messages.error(request, f'Error al editar el clínico: {e}')

        return redirect('ver') 

    return redirect('ver') 

    
    
