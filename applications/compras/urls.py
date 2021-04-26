from django.urls import path , include

from .views import ComprasList, compras ,CompraDetDelete 
from .reportes import reporte_compras ,imprimir_compra

urlpatterns=[
    path('compras/',ComprasList.as_view(), name="lista_compras"),
    path('compras/new',compras, name="nueva_compra"),
    path('compras/edit/<int:compra_id>',compras, name="editar_compra"),
    path('compras/<int:compra_id>/delete/<int:pk>',CompraDetDelete.as_view(), name="delete_detcompra"),
    path('compras/imprimirreportes/' ,reporte_compras, name='imprimirtodas'),
    path('compras/imprimiruna/<int:compra_id>/' , imprimir_compra , name='imprimiruna' ),
]