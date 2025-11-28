# saludos_app/models.py
from django.db import models

class Saludo(models.Model):
    # Un campo de texto para guardar el mensaje
    mensaje = models.CharField(max_length=100)

    def __str__(self):
        # Para que se vea bien en el panel de admin
        return self.mensaje