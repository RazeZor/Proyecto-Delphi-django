from django.shortcuts import render

# Create your views here.
def RenderInforme(request):
    return render(request,'informe.html')