from django.contrib import admin
from .models import Autor, Etiqueta, Articulo, PerfilDeUsuario

# Register your models here.

admin.site.register(Autor)
admin.site.register(Etiqueta)
admin.site.register(Articulo)
admin.site.register(PerfilDeUsuario)