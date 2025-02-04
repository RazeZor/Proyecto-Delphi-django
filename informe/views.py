from django.http import HttpResponse
from django.shortcuts import render


def RenderInforme(request):
    return render(request, 'informe.html')

