from rest_framework import serializers

from applications.productos.models import Producto

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields='__all__'
