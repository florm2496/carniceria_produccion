from django.urls import path , include

from .views import (ClienteNew ,ClienteList , ClienteEdit, \
                        EncVentaList , Ventas ,borrar_detalle_factura,\
                        ListaProductosTablaVenta )
from .reportes import imprimir_factura_recibo ,imprimir_factura_list


urlpatterns = [
    path('clientes/' , ClienteList.as_view() , name='lista_clientes'),
    path('clientes/new/' , ClienteNew.as_view() , name='crear_cliente'),
    path('clientes/<int:pk>' , ClienteEdit.as_view() , name='editar_cliente'),
    path('ventas/' , EncVentaList.as_view() , name='lista_ventas'),
    path('ventas/ventanew/' ,Ventas , name='nueva_venta'),
    path('ventas/ventaedit/<int:id>' ,Ventas , name='editar_venta'),
    #esta es la url del modal de productos
    path('ventas/buscarproductos/' ,ListaProductosTablaVenta  , name='tabla_productos'),
    #path('ventas/buscar_cortes/' ,ListaCortes , name='buscar_cortes'),
    path('ventas/imprimirecibo/<int:id>' , imprimir_factura_recibo ,name='imprimirecibo') ,
    path('ventas/imprimirventas/<str:f1>/<str:f2>/' , imprimir_factura_list , name='imprimirventas'),
    path('ventas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
]