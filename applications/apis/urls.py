from  django.urls import path , include
from .views import ProductosList , ProductoDetalle

urlpatterns=[
    path('v1/productos/' ,ProductosList.as_view() , name='lista_productos_api'),
    path('v1/productos/<str:codigo>', ProductoDetalle.as_view(),name='detalles_productos_api')

]