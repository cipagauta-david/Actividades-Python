# saludos_app/views.py
from django.shortcuts import render
from .models import Saludo # Importamos nuestro Modelo

def mostrar_saludo(request):
    # 1. LÓGICA: Pedir al Modelo (M) el primer saludo que encuentre
    saludo_de_db = Saludo.objects.first() # Obtiene el objeto Saludo que creamos

    # 2. CONTEXTO: Preparar los datos para la Plantilla
    # Creamos un diccionario
    contexto = {
        'saludo_para_template': saludo_de_db
    }

    # 3. RENDER: Enviar la solicitud, la plantilla y los datos
    return render(request, 'saludos_app/saludo.html', contexto)