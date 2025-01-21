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
            respuestaMeses = formulario.curacionDolor.strip().lower()  

            mensaje_section = ""


            
            mensaje = "menos de 3 meses".strip().lower()
            print(respuestaMeses)
            if respuestaMeses == mensaje:
                mensaje_section = (
                    '<div style="color: red; font-weight: bold;">'
                    'Se le aconseja al clínico que este paciente se le realice una derivación a la escala DN4.'
                    '</div>'
                )
            else:
                mensaje_section = (
                    '<div style="color: red; font-weight: bold;">'
                    'No hay consejos en dolor.'
                    '</div>'
                )
            
            
                

            # Leer el archivo HTML
            with open('informe/templates/informe.html', 'r', encoding='utf-8') as template_file:
                informe_template = template_file.read()
            
            # Reemplazar las variables en el HTML usando .format()
            informe = informe_template.format(
                paciente=paciente,
                formulario=formulario,
                mensaje_section=mensaje_section,
            )

            # Añadir el informe al contexto
            context['informe'] = informe
            context['encontrado'] = True

        except (Paciente.DoesNotExist, formularioClinico.DoesNotExist):
            context['encontrado'] = False
            context['mensaje'] = "No se encontró el paciente o su formulario clínico"

    return render(request, 'FichaPacientes.html', context)
