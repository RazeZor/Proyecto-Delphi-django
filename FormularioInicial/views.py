from django.shortcuts import render

def FormularioInicial(request):
    return render(request, 'FormularioInicial.html')

def CuerpoHumano(request):
    return render(request, 'CuerpoHumano.html')