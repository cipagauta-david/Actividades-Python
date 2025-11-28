# mi_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include  # ¡'include' es la clave!

# Importaciones para Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Importación para obtener tokens
from rest_framework.authtoken import views as token_views

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="Documentación de la API del Blog para el Taller de Django",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="profesor@django.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # 1. Nuestras URLs de la App Blog
    path("api/", include("blog.urls")),
    # 2. Endpoint para obtener el Token (Login)
    path("api-token-auth/", token_views.obtain_auth_token),
    # 3. Rutas de Swagger (Documentación)
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("hola/", include("saludos_app.urls")),
    # "Cualquier URL que comience con 'tienda/',
    # reenvíala al archivo 'urls.py' de la app 'tienda'"
    path("tienda/", include("tienda.urls")),
]
