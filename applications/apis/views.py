from django.shortcuts import render

# SE ULTILIZAN LAS API VIEWS .

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .serializers import ProductosSerializer
from applications.productos.models import Producto

class ProductosList(APIView):

    def get(self,request):
        productos=Producto.objects.all()
        data=ProductosSerializer(productos,many=True).data

        return Response(data)

class ProductoDetalle(APIView):
    def get(self, request , codigo):
        print('codigo',codigo)
        if codigo[0]=='7':
            print('es un producto argentino')
            producto=get_object_or_404(Producto,codigo=codigo)   
        elif codigo[0]=='2':
            cod=str(codigo)
            PLU=cod[1:6]
            producto=get_object_or_404(Producto,codigo=PLU)  
        
        data=ProductosSerializer(producto).data
        return Response(data)