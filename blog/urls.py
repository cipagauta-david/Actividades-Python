from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Creamos el router
router = DefaultRouter()

# Registramos nuestras rutas
# El primer argumento es el prefijo de la URL (ej: /api/autores/)
router.register(r"autores", views.AutorViewSet)
router.register(r"etiquetas", views.EtiquetaViewSet)
router.register(r"articulos", views.ArticuloViewSet)
# Mapa de URLs de la app 'blog'
urlpatterns = [
    path("", include(router.urls)),
    # /blog/
    # path("", views.lista_articulos, name="lista_articulos"),
    # /blog/articulo/5/
    path("articulo/<int:pk>/", views.detalle_articulo, name="detalle_articulo"),
    # CRUD Articulo
    path("articulo/nuevo/", views.crear_articulo, name="crear_articulo"),
    path("articulo/<int:pk>/editar/", views.editar_articulo, name="editar_articulo"),
    path(
        "articulo/<int:pk>/eliminar/", views.eliminar_articulo, name="eliminar_articulo"
    ),
]
