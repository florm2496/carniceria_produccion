from django.urls import path , include, re_path
from .views import DetalleCaja, MovimientosCajaCreateView ,ListaOperacionesListView

urlpatterns = [
    
    path('operaciones/' , MovimientosCajaCreateView.as_view() , name='operaciones'),
    path('listaoperaciones/' , ListaOperacionesListView.as_view() , name='listaoperaciones'),
    path('detallecaja/' , DetalleCaja , name='detallecaja'),
   # path('cerrarcaja/' , CerrarCaja , name='cerrarcaja'),
    
]