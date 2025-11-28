# blog/models.py

from django.db import models

from django.contrib.auth.models import User


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


# Cada clase es una tabla en la base de datos.
class Articulo(models.Model):
    # Cada atributo es una columna en la tabla.

    # VARCHAR(200)
    titulo = models.CharField(max_length=200)

    # TEXT
    contenido = models.TextField()

    # DATETIME (se guarda automáticamente al crear)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    # BOOLEAN (con valor por defecto)
    esta_publicado = models.BooleanField(default=True)

    etiquetas = models.ManyToManyField(Etiqueta, related_name="articulos")

    autor = models.ForeignKey(
        Autor,  # El modelo "uno" al que apuntamos
        on_delete=models.CASCADE,  # ¿Qué hacer si se borra el Autor?
        # CASCADE = Borrar todos sus artículos
        related_name="articulos",  # Nombre para acceder "hacia atrás"
        # (desde Autor a sus Artículos)
    )

    def __str__(self):
        # Función mágica de Python para que se vea legible
        # en el panel de admin y en la shell.
        return self.titulo


class PerfilDeUsuario(models.Model):
    # Extiende el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to="perfiles/", blank=True)

    def __str__(self):
        return self.usuario.username
