from django.shortcuts import render
from .models import Producto ,Unidad,Categoria,Marca
# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.views.generic import ListView ,UpdateView, CreateView ,TemplateView
from .forms import UnidadNewForm,ProductoNewForm
from django.urls import reverse_lazy
#,BodegaNewForm 
from django.http import HttpResponse, JsonResponse
from applications.bases.views import SinPrivilegios



class MarcaCreateView(CreateView):
    model = Marca
    template_name = "productos/crearmarca.html"
    fields=('nombre','estado')
    success_url=reverse_lazy('productos:lista_marcas')
    success_message='Marca creada exitosamente'


class MarcaListView(ListView):
    model = Marca
    context_object_name='obj'
    template_name = "productos/lista_marcas.html"


class MarcaEditView(UpdateView):
    model=Marca
    template_name = "productos/crearmarca.html"
    fields=('nombre','estado')
    context_object_name='obj'
    succes_message='Marca editada exitosamente'
    success_url=reverse_lazy('productos:lista_marcas')

class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = "productos/crearcategoria.html"
    fields=('nombre','estado')
    success_url=reverse_lazy('productos:lista_categorias')
    success_message='Categoria creada exitosamente'

class CategoriaListView(ListView):
    model = Categoria
    context_object_name='obj'
    template_name = "productos/lista_categorias.html"


class CategoriaEditView(UpdateView):
    model = Categoria
    template_name = "productos/crearcategoria.html"
    context_object_name='obj'
    fields=('nombre','estado')
    success_url=reverse_lazy('productos:lista_categorias')
    success_message='Categoria editada exitosamente'



class MixinFormInvalid():
    def form_invalid(self , form):
        response=super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors , status=400)
        else:
            return response 



class UnidadList(SuccessMessageMixin,SinPrivilegios,ListView):
    model=Unidad
    context_object_name='obj'
    template_name='productos/lista_unidades.html'
    login_url='bases:login'
    permission_required='producto.view_unidad'
    
class UnidadNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=Unidad
    form_class=UnidadNewForm
    context_object_name='obj'
    template_name='productos/crearunidad.html'
    success_url=reverse_lazy('productos:lista_unidades')
   
    permission_required='producto.add_unidad'
    success_message='Unidad creada exitosamente'
class UnidadUpdate(SuccessMessageMixin,SinPrivilegios,UpdateView):
    model=Unidad
    form_class=UnidadNewForm
    context_object_name='obj'
    template_name='productos/crearunidad.html'
    success_url=reverse_lazy('productos:lista_unidades')

    permission_required='producto.change_unidad'
    success_message='Unidad editada exitosamente'

    

class ProductoList(SuccessMessageMixin,SinPrivilegios,ListView): 
    model=Producto
    context_object_name='obj'
    template_name='productos/productos.html'
    login_url='bases:login'
    permission_required='producto.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = Producto.objects.filter(tipo='mercaderia',estado=True)
        return context

class CortesListView(SuccessMessageMixin,SinPrivilegios,ListView):
    model=Producto
    context_object_name='obj'
    template_name='productos/cortesdecarne.html'
    login_url='bases:login'
    permission_required='producto.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cortes"] = Producto.objects.filter(tipo='carne',estado=True)
        return context

       

    
class ProductoNew(SuccessMessageMixin,MixinFormInvalid,SinPrivilegios,CreateView): 
    model=Producto
    form_class=ProductoNewForm
    context_object_name='obj'
    template_name='productos/modalproducto.html'
    success_url=reverse_lazy('productos:lista_productos')
    login_url='bases:login'
    permission_required='producto.add_producto'
    success_message='Producto creado exitosamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    
    def get_context_data(self , **kwargs):
        context=super(ProductoNew , self).get_context_data(**kwargs)
        context['unidades']=Unidad.objects.filter(estado=True)
        context['categorias']=Categoria.objects.filter(estado=True)
        context['marcas']=Marca.objects.filter(estado=True)
        return context

class ProductoUpdate(SuccessMessageMixin, MixinFormInvalid,SinPrivilegios,UpdateView): 
    model=Producto
    form_class=ProductoNewForm
    context_object_name='obj'
    template_name='productos/modalproducto.html'
    success_url=reverse_lazy('productos:lista_productos')
    login_url='bases:login'
    permission_required='producto.change_producto'
    success_message='Producto editado exitosamente'
    #permission_required='vino.delete_vino'
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super(ProductoUpdate , self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['unidades']=Unidad.objects.filter(estado=True)
        context['categorias']=Categoria.objects.filter(estado=True)
        context['marcas']=Marca.objects.filter(estado=True)
        context["obj"] = Producto.objects.filter(pk=pk).first()
        return context