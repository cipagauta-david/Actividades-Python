from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ArticuloForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Autor, Etiqueta, Articulo
from .serializers import AutorSerializer, EtiquetaSerializer, ArticuloSerializer


def lista_articulos(request):
	articulos = Articulo.objects.select_related("autor").prefetch_related("etiquetas").all().order_by("-fecha_publicacion")
	return render(request, "blog/lista_articulos.html", {"articulos": articulos})


def detalle_articulo(request, pk: int):
	articulo = get_object_or_404(Articulo.objects.select_related("autor").prefetch_related("etiquetas"), pk=pk)
	return render(request, "blog/detalle_articulo.html", {"articulo": articulo})


def crear_articulo(request):
	if request.method == "POST":
		form = ArticuloForm(request.POST)
		if form.is_valid():
			articulo = form.save()
			return redirect(reverse("detalle_articulo", args=[articulo.pk]))
	else:
		form = ArticuloForm()
	return render(request, "blog/articulo_form.html", {"form": form, "modo": "Crear"})


def editar_articulo(request, pk: int):
	articulo = get_object_or_404(Articulo, pk=pk)
	if request.method == "POST":
		form = ArticuloForm(request.POST, instance=articulo)
		if form.is_valid():
			articulo = form.save()
			return redirect(reverse("detalle_articulo", args=[articulo.pk]))
	else:
		form = ArticuloForm(instance=articulo)
	return render(request, "blog/articulo_form.html", {"form": form, "modo": "Editar", "articulo": articulo})


def eliminar_articulo(request, pk: int):
	articulo = get_object_or_404(Articulo, pk=pk)
	if request.method == "POST":
		articulo.delete()
		return redirect(reverse("lista_articulos"))
	return render(request, "blog/articulo_confirm_delete.html", {"articulo": articulo})

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios con Token entran

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [IsAuthenticated]

class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    # Permitimos leer a cualquiera, pero editar solo si estás autenticado
    permission_classes = [IsAuthenticatedOrReadOnly]