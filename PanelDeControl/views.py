from django.shortcuts import render

def panel(request):
    return render(request, 'panel.html')  # Renderiza la plantilla panel.html en la respuesta HTTP.

