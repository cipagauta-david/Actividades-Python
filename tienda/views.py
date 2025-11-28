from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def lista_productos(request):
	"""Vista simple que lista productos disponibles."""
	return HttpResponse("Lista de productos de la tienda")


def detalle_producto(request, pk: int):
	"""Vista simple para el detalle de un producto identificado por pk."""
	return HttpResponse(f"Detalle del producto {pk}")
