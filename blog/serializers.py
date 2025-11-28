from rest_framework import serializers
from .models import Autor, Etiqueta, Articulo

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__' # Serializa todos los campos

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class ArticuloSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre del autor en lugar de solo su ID (Opcional)
    # autor = serializers.StringRelatedField() 
    
    class Meta:
        model = Articulo
        fields = '__all__'
        # Si quieres incluir los campos anidados (que se vea todo el objeto autor, no solo el ID)
        # depth = 1