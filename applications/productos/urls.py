from django.urls import path , include 
from .views import UnidadList,UnidadNew,UnidadUpdate ,ProductoNew,ProductoList,ProductoUpdate,CategoriaCreateView,CategoriaListView,MarcaCreateView,MarcaListView,CategoriaEditView,MarcaEditView,CortesListView
from django.contrib.auth import views as auth_views


urlpatterns = [
  
    path('unidades/',UnidadList.as_view(),name='lista_unidades'),
    path('unidades/unidadnew',UnidadNew.as_view(),name='crear_unidad'),
    path('unidades/unidadupdate/<int:pk>/',UnidadUpdate.as_view(),name='editar_unidad'),
 
    path('productos/',ProductoList.as_view(),name='lista_productos'),
    path('productos/new/',ProductoNew.as_view(),name='crear_producto'),
    path('productos/actualizar/<int:pk>',ProductoUpdate.as_view(),name='actualizar_producto'),

    path('productos/marcas/' ,MarcaListView.as_view(),name='lista_marcas'),
    path('productos/crearmarca/' ,MarcaCreateView.as_view(),name='crearmarca'),
    path('productos/editarmarca/<int:pk>' ,MarcaEditView.as_view(),name='editar_marca'),

    path('productos/categorias/' ,CategoriaListView.as_view(),name='lista_categorias'), 
    path('productos/crearcategoria/' ,CategoriaCreateView.as_view(),name='crearcategoria'),
    path('productos/editarcategoria/<int:pk>' ,CategoriaEditView.as_view(),name='editar_categoria'),

    path('productos/cortesdecarne/',CortesListView.as_view() ,name='lista_cortes' )
]