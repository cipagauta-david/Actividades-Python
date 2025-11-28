from django import forms
from .models import Articulo


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "contenido",
            "esta_publicado",
            "autor",
            "etiquetas",
        ]
        widgets = {
            "contenido": forms.Textarea(attrs={"rows": 6}),
        }
