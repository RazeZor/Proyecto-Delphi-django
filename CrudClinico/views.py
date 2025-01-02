from pyexpat.errors import messages
from django.shortcuts import render
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
            
        except Exception as e:
            messages.error(request, f'Error al agregar el clínico: {e}')
    return render(request, 'AgregarClinico.html')

def VerClinicos(request):
    clinicos = Clinico.objects.all()
    return render(request, 'VerClinicos.html', {'clinicos': clinicos})

def eliminarClinico(request, rut):
    clinico = Clinico.objects.get(rut=rut)
    clinico.delete()
    return render(request, 'VerClinicos.html')


    
    
