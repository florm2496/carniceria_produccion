from django.urls import path , include, re_path
from .views import (TropaNew,TropaUpdate,TropasList,\
                    AnimalNew,AnimalesList, \
                    ResesList,ResUpdate, \
                   VentaReses,ListaVentasReses,PagoVentaAjax,CrearPagoCliente,ListaPagosCliente)

urlpatterns = [
   
    path('tropas/' ,TropasList.as_view() , name='lista_tropas'),
    path('añadirtropa/' ,TropaNew.as_view() , name='crear_tropa'),
    path('editartropa/<int:pk>' ,TropaUpdate.as_view() , name='editar_tropa'),

    #path('animal/<int:pk>' ,AñadirAnimal.as_view() , name='animal'),
    path('animal/<int:pk>' ,AnimalNew , name='animal'),
    path('animales/<int:pk>' ,AnimalesList.as_view() , name='animales'),

     #path('registrares/' , ResCreateView.as_view() , name='registrares'),
    path('listareses/' , ResesList.as_view() , name='lista_reses'),
    path('updatereses/<int:pk>' ,ResUpdate.as_view() , name='editar_res'),
    #nueva vista para vender res (vista por funciones)

    path('nuevaventares/' ,VentaReses , name='nuevaventares'),
    path('editarventares/<int:id>' ,VentaReses , name='editarventares'),
    path('listaventas/',ListaVentasReses.as_view(),name='listaventas'),

    #prueba
    path('pagoventa/',PagoVentaAjax,name='pago_venta_ajax'),
    #path('pagocliente/<int:id>',PagoCliente,name='pago_cliente'),
    path('CrearPagoCliente/<int:id>',CrearPagoCliente.as_view(),name='crearpagocliente'),
    path('listapagos/<int:id>' ,ListaPagosCliente.as_view(),name='listapagos')
]