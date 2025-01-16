import json
from django.shortcuts import render, redirect
from Login.models import Paciente, formularioClinico
from django.http import HttpResponse, JsonResponse


def panel(request):
    if 'nombre_clinico' in request.session:
        nombre_clinico = request.session['nombre_clinico']
        es_admin = request.session.get('es_admin', False)
        return render(request, 'panel.html', {'nombre_clinico': nombre_clinico, 'es_admin': es_admin})
    else:
        return redirect('login')
    
def cerrar_sesion(request):
    # Elimina todos los datos de la sesión
    request.session.flush()
    
    # Redirige al login (o a cualquier otra página que desees)
    return redirect('login')  # Asegúrate de que 'login' sea el nombre de tu URL de login

def VerFichaPacientes(request):
    if 'nombre_clinico' not in request.session:
        return redirect('login')
    
    nombre_clinico = request.session['nombre_clinico']
    rut = request.GET.get('rut', None)
    context = {'nombre_clinico': nombre_clinico}
    
    if rut:
        try:
            paciente = Paciente.objects.get(rut=rut)
            formulario = formularioClinico.objects.get(paciente=paciente)
            
        
            with open('informe/templates/informe.html', 'r', encoding='utf-8') as template_file:
                informe_template = template_file.read()
            
            informe = informe_template.format(
                paciente=paciente,
                formulario=formulario
            )

            context['informe'] = informe
            context['encontrado'] = True

        
            
        except (Paciente.DoesNotExist, formularioClinico.DoesNotExist):
            context['encontrado'] = False
            context['mensaje'] = "No se encontró el paciente o su formulario clínico"
    
    return render(request, 'FichaPacientes.html', context)
