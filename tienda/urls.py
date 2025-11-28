from django.urls import path
from . import views

# Mapa de URLs de la app 'tienda'
urlpatterns = [
    # /tienda/
    path('', views.lista_productos, name='lista_productos'),

    # /tienda/producto/10/
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
]
