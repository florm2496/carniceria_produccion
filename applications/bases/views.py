from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum ,Q
from applications.ventas.models import FacturaEnc , FacturaDet ,Cliente
from applications.productos.models import Producto
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin





class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception=False
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin,generic.TemplateView):
    template_name='bases/home.html'
    login_url='bases:login'

class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"


def Dashboard(request):
    template_name='bases/dashboard.html'
    context={}
    
    prods=Producto.objects.all().count()
    ultimos_prod=Producto.objects.all().order_by('-fc')[:3]

    facs=FacturaEnc.objects.aggregate(Sum('total'))
    
    if facs['total__sum'] is None:
        facs['total__sum']=0
    else:
        pass

    total_ventas=facs['total__sum']
    ventas_registradas=FacturaEnc.objects.count()
    users=User.objects.all()
    client=Cliente.objects.all().count()
    
    mv=FacturaDet.objects.values('producto__nombre' ,'producto__codigo').annotate(Sum('cantidad'))
    sinstock=Producto.objects.filter(existencia=0)

   
    valores=[]
    for objeto in Producto.objects.all():
        sm=objeto.sm
        if sm != None:
            if objeto.existencia < objeto.sm and objeto.existencia>0:
                queryset=Producto.objects.filter(Q(existencia__lt = sm ) & Q(existencia__gt = 0 ) )
                valores.append(queryset)
    if len(valores)==0:
        val=[0]
    elif len(valores)!=0:
        val=valores[0]
    #def UltimosMovimientos():
    ultimas_mod=Producto.objects.all().order_by('-fm')[:5]
    print(ultimas_mod)

    
    context={
        'prods':prods,
        'facs':total_ventas,
        'users':users,
        'client':client,
        'up':ultimos_prod,
        'mv':mv,
        'ss':sinstock,
        'sm':val,
        'um':ultimas_mod,
        'vr':ventas_registradas,
    }

    return render(request, template_name, context)
