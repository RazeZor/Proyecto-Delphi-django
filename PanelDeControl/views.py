from django.shortcuts import redirect, render

def panel(request):
    if 'nombre_clinico' in request.session:
        nombre_clinico = request.session['nombre_clinico']
        return render(request, 'panel.html', {'nombre_clinico': nombre_clinico})
    else:
        return redirect('login')
    
def cerrar_sesion(request):
    # Elimina todos los datos de la sesión
    request.session.flush()
    
    # Redirige al login (o a cualquier otra página que desees)
    return redirect('login')  # Asegúrate de que 'login' sea el nombre de tu URL de login